"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: render_pipeline.py                                 ║
║   Função: Orquestrador Universal de Render (6 etapas)        ║
║   LAYER 1 — Task 1.2                                         ║
╚══════════════════════════════════════════════════════════════╝

USAGE (inside any Blender script):
    import sys
    sys.path.append("D:/Blender/blenderscripts/scripts/utils")
    from render_pipeline import RenderPipeline

    pipe = RenderPipeline(output_path="D:/renders/my_video.mp4")

    # Wrap your scene-building code:
    def build():
        # ... all your bpy calls ...
        pass

    result = pipe.run(build_fn=build)
    # result = {"status": "PASS", "output": "...", "size_bytes": ..., ...}

HEADLESS COMPATIBLE: Yes — works with blender -b -P
"""

import bpy
import os
import sys
import json
import time
from datetime import datetime


class RenderPipeline:
    """
    6-step render orchestrator:
      1. BUILD   → call user's scene-building function
      2. VALIDATE → pre-render checks (camera, lights, objects)
      3. PREVIEW  → optional single-frame preview check
      4. RENDER   → full animation or still
      5. VERIFY   → post-render output check
      6. REPORT   → write JSON report to disk
    """

    def __init__(self,
                 output_path: str,
                 engine: str = "BLENDER_EEVEE_NEXT",
                 frame_start: int = None,
                 frame_end: int = None,
                 resolution: tuple = (1920, 1080),
                 fps: int = 24,
                 report_dir: str = "D:/Blender/blenderscripts/renders/tests"):
        self.output_path = output_path
        self.engine      = engine
        self.frame_start = frame_start
        self.frame_end   = frame_end
        self.resolution  = resolution
        self.fps         = fps
        self.report_dir  = report_dir

        self.scene       = bpy.context.scene
        self.timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report      = {
            "timestamp":       self.timestamp,
            "output_path":     output_path,
            "status":          "PENDING",
            "steps":           [],
            "errors":          [],
            "warnings":        [],
            "duration_sec":    0,
            "output_size_bytes": 0,
        }
        self._t_start = time.time()

    # ─────────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────────

    def run(self, build_fn=None, preview: bool = False) -> dict:
        """Run the full 6-step pipeline. Returns report dict."""
        print("\n" + "═" * 56)
        print("  🎬 FGS RENDER PIPELINE — Starting")
        print("═" * 56)

        try:
            # 1 BUILD
            self._step_build(build_fn)

            # 2 VALIDATE
            ok = self._step_validate()
            if not ok:
                return self._finish("FAIL_VALIDATION")

            # 3 PREVIEW (optional — renders frame 1)
            if preview:
                ok = self._step_preview()
                if not ok:
                    return self._finish("FAIL_PREVIEW")

            # 4 RENDER
            ok = self._step_render()
            if not ok:
                return self._finish("FAIL_RENDER")

            # 5 VERIFY
            ok = self._step_verify()
            if not ok:
                return self._finish("FAIL_OUTPUT")

            return self._finish("PASS")

        except Exception as e:
            self._log(f"Unhandled exception: {e}", ok=False)
            return self._finish("FAIL_EXCEPTION")

    # ─────────────────────────────────────────────────
    # STEP 1 — BUILD
    # ─────────────────────────────────────────────────

    def _step_build(self, build_fn):
        print("\n[1/6] BUILD")
        if build_fn:
            try:
                build_fn()
                self._log("Scene build function executed")
            except Exception as e:
                self._log(f"Build function error: {e}", ok=False)
                raise
        else:
            self._log("No build function provided — using existing scene")

    # ─────────────────────────────────────────────────
    # STEP 2 — VALIDATE (pre-render checks)
    # ─────────────────────────────────────────────────

    def _step_validate(self) -> bool:
        print("\n[2/6] VALIDATE")
        ok = True

        # Camera
        if not self.scene.camera:
            self._log("No active camera", ok=False)
            ok = False
        else:
            self._log(f"Camera: {self.scene.camera.name} ✓")

        # Camera can see something (basic check)
        cam = self.scene.camera
        if cam:
            mesh_objs = [o for o in self.scene.objects
                         if o.type == 'MESH' and not o.hide_render]
            if not mesh_objs:
                self._log("No visible mesh objects for camera", ok=False)
                ok = False
            else:
                self._log(f"Visible meshes: {len(mesh_objs)} ✓")

        # Lights
        lights = [o for o in self.scene.objects
                  if o.type == 'LIGHT' and not o.hide_render]
        if not lights:
            self._warn("No lights found — render will be black")
        else:
            self._log(f"Lights: {len(lights)} ✓")

        # Output path directory
        out_dir = os.path.dirname(self.output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            self._log(f"Output dir ready: {out_dir} ✓")

        return ok

    # ─────────────────────────────────────────────────
    # STEP 3 — PREVIEW (single frame to check visuals)
    # ─────────────────────────────────────────────────

    def _step_preview(self) -> bool:
        print("\n[3/6] PREVIEW (single frame)")
        prev_path = self.output_path.rsplit('.', 1)[0] + "_preview.png"

        old_path   = self.scene.render.filepath
        old_format = self.scene.render.image_settings.file_format
        old_frame  = self.scene.frame_current

        self.scene.render.filepath = prev_path
        self.scene.render.image_settings.file_format = 'PNG'
        self.scene.frame_set(self.scene.frame_start)

        try:
            bpy.ops.render.render(write_still=True)
        except Exception as e:
            self._log(f"Preview render failed: {e}", ok=False)
            return False
        finally:
            self.scene.render.filepath = old_path
            self.scene.render.image_settings.file_format = old_format
            self.scene.frame_set(old_frame)

        if os.path.exists(prev_path) and os.path.getsize(prev_path) > 5000:
            self._log(f"Preview OK: {os.path.getsize(prev_path):,} bytes ✓")
            return True
        else:
            self._log("Preview output missing or too small", ok=False)
            return False

    # ─────────────────────────────────────────────────
    # STEP 4 — RENDER
    # ─────────────────────────────────────────────────

    def _step_render(self) -> bool:
        print("\n[4/6] RENDER")
        self._apply_settings()

        try:
            bpy.ops.render.render(animation=(self.scene.frame_start != self.scene.frame_end),
                                  write_still=True)
            self._log("Render completed ✓")
            return True
        except Exception as e:
            self._log(f"Render exception: {e}", ok=False)
            return False

    # ─────────────────────────────────────────────────
    # STEP 5 — VERIFY (post-render output check)
    # ─────────────────────────────────────────────────

    def _step_verify(self) -> bool:
        print("\n[5/6] VERIFY")

        # For animations, Blender writes numbered frames or the container file
        check_path = self.output_path

        # PNG sequence? Check for first frame file
        if "#" in self.output_path:
            first = self.output_path.replace("####", "0001")
            check_path = first

        if not os.path.exists(check_path):
            self._log(f"Output not found: {check_path}", ok=False)
            return False

        size = os.path.getsize(check_path)
        self.report["output_size_bytes"] = size

        MIN_SIZE = 5000  # 5KB absolute minimum
        if size < MIN_SIZE:
            self._log(f"Output suspiciously small ({size} bytes) — possible blank render", ok=False)
            return False

        self._log(f"Output file: {size:,} bytes ✓")
        return True

    # ─────────────────────────────────────────────────
    # STEP 6 — REPORT
    # ─────────────────────────────────────────────────

    def _finish(self, status: str) -> dict:
        self.report["status"]       = status
        self.report["duration_sec"] = round(time.time() - self._t_start, 2)

        os.makedirs(self.report_dir, exist_ok=True)
        report_path = f"{self.report_dir}/render_report_{self.timestamp}.json"
        with open(report_path, 'w') as f:
            json.dump(self.report, f, indent=2)

        passed = status == "PASS"
        print("\n" + "═" * 56)
        if passed:
            print(f"  ✅ PIPELINE PASSED in {self.report['duration_sec']}s")
            print(f"     Output: {self.output_path}")
        else:
            print(f"  ❌ PIPELINE FAILED: {status}")
            for e in self.report["errors"]:
                print(f"     • {e}")
        print(f"  📋 Report: {report_path}")
        print("═" * 56)

        return self.report

    # ─────────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────────

    def _apply_settings(self):
        """Apply render settings from constructor parameters."""
        s = self.scene
        s.render.engine = self.engine
        s.render.resolution_x = self.resolution[0]
        s.render.resolution_y = self.resolution[1]
        s.render.fps = self.fps
        s.render.filepath = self.output_path

        if self.frame_start is not None:
            s.frame_start = self.frame_start
        if self.frame_end is not None:
            s.frame_end = self.frame_end

        # Format detection from extension
        ext = self.output_path.lower().rsplit('.', 1)[-1]
        fmt_map = {
            'png':  ('PNG', None),
            'jpg':  ('JPEG', None),
            'jpeg': ('JPEG', None),
            'mp4':  ('FFMPEG', 'MPEG4'),
            'mov':  ('FFMPEG', 'QUICKTIME'),
            'webm': ('FFMPEG', 'WEBM'),
        }
        if ext in fmt_map:
            fmt, container = fmt_map[ext]
            s.render.image_settings.file_format = fmt
            if container:
                s.render.ffmpeg.format = container
                s.render.ffmpeg.codec  = 'H264'
                s.render.ffmpeg.audio_codec = 'AAC'
        self._log(f"Engine: {self.engine} | Res: {self.resolution[0]}x{self.resolution[1]} | FPS: {self.fps}")

    def _log(self, msg: str, ok: bool = True):
        symbol = "✅" if ok else "❌"
        print(f"   {symbol} {msg}")
        self.report["steps"].append({"ok": ok, "msg": msg})
        if not ok:
            self.report["errors"].append(msg)

    def _warn(self, msg: str):
        print(f"   ⚠️  {msg}")
        self.report["warnings"].append(msg)


# ─────────────────────────────────────────────────────────────
# STANDALONE EXECUTION — Quick integration test
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import bmesh

    def build_test_scene():
        """Minimal scene to test the pipeline itself."""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Sphere
        mesh = bpy.data.meshes.new("Test_Sphere")
        obj  = bpy.data.objects.new("Test_Sphere", mesh)
        bpy.context.scene.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
        bm.to_mesh(mesh)
        bm.free()

        mat = bpy.data.materials.new("Test_Mat")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        p = nodes.new("ShaderNodeBsdfPrincipled")
        o = nodes.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(p.outputs["BSDF"], o.inputs["Surface"])
        p.inputs["Base Color"].default_value = (0.8, 0.2, 0.05, 1.0)
        p.inputs["Roughness"].default_value  = 0.4
        obj.data.materials.append(mat)

        # Light
        ld = bpy.data.lights.new("L", type='POINT')
        ld.energy = 500
        lo = bpy.data.objects.new("L", ld)
        bpy.context.scene.collection.objects.link(lo)
        lo.location = (3, -3, 4)

        # Camera
        cd = bpy.data.cameras.new("C")
        co = bpy.data.objects.new("C", cd)
        bpy.context.scene.collection.objects.link(co)
        co.location = (4, -4, 3)
        co.rotation_euler = (1.1, 0.0, 0.8)
        bpy.context.scene.camera = co

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pipe = RenderPipeline(
        output_path=f"D:/Blender/blenderscripts/renders/tests/pipeline_test_{ts}.png",
        engine="BLENDER_EEVEE_NEXT",
        frame_start=1,
        frame_end=1,
        resolution=(1280, 720),
    )
    result = pipe.run(build_fn=build_test_scene, preview=False)
    sys.exit(0 if result["status"] == "PASS" else 1)
