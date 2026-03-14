# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: lorena_avatar.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Personagens                       ║
║   Script: lorena_avatar.py                                  ║
║   Função: Avatar IA Holográfica "Lorena"                    ║
║           Rig completo, Shape Keys faciais, Lip Sync        ║
║           Integrado com AnimationEngine + MaterialLibrary    ║
╚══════════════════════════════════════════════════════════════╝

NVIDIA RECOMMENDATION — P0 Task:
Create Lorena with full rig, shape keys, and lip_sync()
to unlock the complete animation pipeline.

USO (dentro do Blender):
    import sys
    from pathlib import Path
    # Determine base relative to this file
    BASE = Path(__file__).resolve().parents[2]
    sys.path.append(str(BASE / "scripts" / "utils"))
    from lorena_avatar import LorenaAvatar
"""

import bpy
import math
import os
import sys
import wave
import struct

from pathlib import Path
from mathutils import Vector, Euler

# Setup paths
try:
    from paths import BASE_DIR, UTILS_DIR
    from logger import get_logger
    
    log = get_logger("LORENA_AVATAR")
    FGS_ROOT = BASE_DIR
    if str(UTILS_DIR) not in sys.path:
        sys.path.append(str(UTILS_DIR))
except ImportError:
    FGS_ROOT = Path(__file__).resolve().parents[2]
    sys.path.append(str(FGS_ROOT / "scripts" / "utils"))
    log = None # Fallback to print if logger fails

try:
    from animation_engine import AnimationEngine
    from materials_library import MaterialLibrary
except ImportError as e:
    print(f"⚠️ Dependência não encontrada (normal fora do Blender): {e}")
    AnimationEngine = None
    MaterialLibrary = None


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────
LORENA_COLOR       = (0.05, 0.7, 1.0)    # Azul ciano holográfico
LORENA_OPACITY     = 0.35
LORENA_HEIGHT      = 1.75                # metros
LORENA_FPS         = 24

# Shape Keys disponíveis (visemes + expressões)
SHAPE_KEYS = ["smile", "angry", "surprise", "blink", "mouth_open", "mouth_ah",
              "mouth_oh", "mouth_closed", "brow_up", "brow_down"]

# Mapeamento Rhubarb → Shape Keys do FGS
# Fonemas Rhubarb: A(ah), B(closed), C(ee), D(ih), E(oh), F(oo), G(uh), H(schwa), X(silence)
RHUBARB_VISEME_MAP = {
    "A": {"mouth_ah": 0.9, "mouth_open": 0.6},
    "B": {"mouth_closed": 1.0},
    "C": {"mouth_open": 0.4},
    "D": {"mouth_open": 0.3},
    "E": {"mouth_oh": 0.8, "mouth_open": 0.5},
    "F": {"mouth_oh": 0.6},
    "G": {"mouth_open": 0.45},
    "H": {"mouth_open": 0.2},
    "X": {"mouth_closed": 0.8},
}


# ─────────────────────────────────────────────────────────────────────────────
# LORENA AVATAR
# ─────────────────────────────────────────────────────────────────────────────
class LorenaAvatar:
    """
    Avatar IA Holográfica Lorena.
    
    Cria um personagem humanoide holográfico completo com:
    - Geometria base (corpo + cabeça)
    - Armature (rig básico compatível com BVH)
    - Shape Keys faciais (expressões + visemes para lip sync)
    - Material holográfico (azul ciano translúcido)
    - Integração com AnimationEngine para idle e animações de fundo
    """

    def __init__(self, nome="Lorena", posicao=(0, 0, 0)):
        self.nome = nome
        self.posicao = posicao
        self.mesh_obj = None
        self.armature_obj = None
        self.material = None

        # Inicializa engines se disponíveis
        if AnimationEngine:
            self.anim = AnimationEngine(fps=LORENA_FPS)
        else:
            self.anim = None

        if MaterialLibrary:
            self.lib = MaterialLibrary()
        else:
            self.lib = None

    # ───────────────────────────── BUILD ─────────────────────────────────────

    def build(self) -> None:
        """Constrói o avatar completo na cena."""
        print(f"\n✨ Construindo avatar: {self.nome}...")

        self._limpar_cena_lorena()
        self._criar_geometria()
        self._criar_armature()
        self._aplicar_parenting()
        self._criar_shape_keys()
        self._aplicar_material()

        print(f"✅ {self.nome} construída com sucesso!")
        print(f"   Mesh: {self.mesh_obj.name}")
        print(f"   Rig:  {self.armature_obj.name}")
        print(f"   Shape Keys: {len(SHAPE_KEYS)}")

    # ──────────────────── GEOMETRIA ──────────────────────────────────────────

    def _limpar_cena_lorena(self):
        """Remove objetos Lorena anteriores para rebuild limpo."""
        for obj in list(bpy.data.objects):
            if self.nome in obj.name:
                bpy.data.objects.remove(obj, do_unlink=True)

    def _criar_geometria(self) -> None:
        """Cria a geometria base: corpo cilíndrico + cabeça esférica."""
        # Corpo
        height = LORENA_HEIGHT * 0.55
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.18,
            depth=height,
            location=(self.posicao[0], self.posicao[1], self.posicao[2] + height / 2 + 0.02)
        )
        corpo = bpy.context.active_object
        corpo.name = f"{self.nome}_Corpo"

        # Cabeça
        head_z = self.posicao[2] + height + 0.28
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.22,
            segments=24, ring_count=16,
            location=(self.posicao[0], self.posicao[1], head_z)
        )
        cabeca = bpy.context.active_object
        cabeca.name = f"{self.nome}_Cabeca"

        # Pescoço (conector)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.06,
            depth=0.12,
            location=(self.posicao[0], self.posicao[1], self.posicao[2] + height + 0.06)
        )
        pescoco = bpy.context.active_object
        pescoco.name = f"{self.nome}_Pescoco"

        # Join em único mesh
        bpy.ops.object.select_all(action='DESELECT')
        for obj in [corpo, pescoco]:  # Cabeça é o ativo
            obj.select_set(True)
        cabeca.select_set(True)
        bpy.context.view_layer.objects.active = cabeca
        bpy.ops.object.join()

        self.mesh_obj = bpy.context.active_object
        self.mesh_obj.name = f"{self.nome}_Mesh"

    # ──────────────────── ARMATURE ───────────────────────────────────────────

    def _criar_armature(self) -> None:
        """Cria armature hierárquica básica para animação e mocap BVH."""
        bpy.ops.object.armature_add(enter_editmode=True, location=self.posicao)
        self.armature_obj = bpy.context.active_object
        self.armature_obj.name = f"{self.nome}_Rig"
        self.armature_obj.show_in_front = True

        arm = self.armature_obj.data
        arm.name = f"{self.nome}_Armature"
        arm.display_type = 'STICK'

        # Remove bone padrão
        bpy.ops.armature.delete()

        h = LORENA_HEIGHT
        px, py, pz = self.posicao

        # Define bones como (nome, head, tail, parent_name)
        bones_def = [
            ("root",      (px,   py, pz),          (px,   py, pz+0.1),   None),
            ("pelvis",    (px,   py, pz+0.1),       (px,   py, pz+0.4),   "root"),
            ("spine_1",   (px,   py, pz+0.4),       (px,   py, pz+0.7),   "pelvis"),
            ("spine_2",   (px,   py, pz+0.7),       (px,   py, pz+1.0),   "spine_1"),
            ("chest",     (px,   py, pz+1.0),       (px,   py, pz+1.2),   "spine_2"),
            ("neck",      (px,   py, pz+1.2),       (px,   py, pz+1.4),   "chest"),
            ("head",      (px,   py, pz+1.4),       (px,   py, pz+1.75),  "neck"),
            ("jaw",       (px,   py, pz+1.45),      (px,   py+0.05, pz+1.35), "head"),
            # Braços
            ("L_shoulder",(px-0.05, py, pz+1.1),   (px-0.3, py, pz+1.1), "chest"),
            ("L_upper_arm",(px-0.3, py, pz+1.1),   (px-0.6, py, pz+1.0), "L_shoulder"),
            ("L_forearm", (px-0.6, py, pz+1.0),    (px-0.85, py, pz+0.85), "L_upper_arm"),
            ("R_shoulder",(px+0.05, py, pz+1.1),   (px+0.3, py, pz+1.1), "chest"),
            ("R_upper_arm",(px+0.3, py, pz+1.1),   (px+0.6, py, pz+1.0), "R_shoulder"),
            ("R_forearm", (px+0.6, py, pz+1.0),    (px+0.85, py, pz+0.85), "R_upper_arm"),
        ]

        # Cria bones
        created = {}
        for b_name, head, tail, parent in bones_def:
            bone = arm.edit_bones.new(b_name)
            bone.head = Vector(head)
            bone.tail = Vector(tail)
            if parent and parent in created:
                bone.parent = created[parent]
                bone.use_connect = False
            created[b_name] = bone

        bpy.ops.object.editmode_toggle()

    def _aplicar_parenting(self) -> None:
        """Parent do mesh ao armature com Weight Paint automático."""
        bpy.ops.object.select_all(action='DESELECT')
        self.mesh_obj.select_set(True)
        self.armature_obj.select_set(True)
        bpy.context.view_layer.objects.active = self.armature_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        print("   🦴 Rig vinculado ao mesh (Auto Weights)")

    # ──────────────────── SHAPE KEYS ─────────────────────────────────────────

    def _criar_shape_keys(self) -> None:
        """Cria todas as shape keys faciais para expressões e lip sync."""
        bpy.context.view_layer.objects.active = self.mesh_obj
        self.mesh_obj.select_set(True)

        # Garante Base
        if not self.mesh_obj.data.shape_keys:
            self.mesh_obj.shape_key_add(name="Basis")

        # Face verts (extremidade superior do mesh = zona facial)
        face_verts_idx = [
            v.index for v in self.mesh_obj.data.vertices
            if v.co.z > (LORENA_HEIGHT * 0.75)
        ]
        mouth_verts_idx = [
            v.index for v in self.mesh_obj.data.vertices
            if v.co.z > (LORENA_HEIGHT * 0.77) and v.co.z < (LORENA_HEIGHT * 0.87)
        ]
        brow_verts_idx = [
            v.index for v in self.mesh_obj.data.vertices
            if v.co.z > (LORENA_HEIGHT * 0.93)
        ]

        sk_configs = {
            "smile":        (mouth_verts_idx, Vector((0, -0.015, 0.01))),
            "angry":        (brow_verts_idx,  Vector((0, 0, -0.02))),
            "surprise":     (brow_verts_idx,  Vector((0, 0, 0.025))),
            "blink":        (brow_verts_idx,  Vector((0, 0.01, -0.015))),
            "mouth_open":   (mouth_verts_idx, Vector((0, 0.02, -0.01))),
            "mouth_ah":     (mouth_verts_idx, Vector((0, 0.025, -0.015))),
            "mouth_oh":     (mouth_verts_idx, Vector((0, 0.015, -0.008))),
            "mouth_closed": (mouth_verts_idx, Vector((0, -0.01, 0.005))),
            "brow_up":      (brow_verts_idx,  Vector((0, 0, 0.018))),
            "brow_down":    (brow_verts_idx,  Vector((0, 0, -0.018))),
        }

        for sk_name, (vert_indices, offset) in sk_configs.items():
            sk = self.mesh_obj.shape_key_add(name=sk_name)
            sk.interpolation = 'KEY_LINEAR'
            # Desloca verts relevantes para criar a forma
            for vi in vert_indices:
                sk.data[vi].co += offset

        print(f"   😊 {len(sk_configs)} Shape Keys criadas")

    # ──────────────────── MATERIAL ───────────────────────────────────────────

    def _aplicar_material(self) -> None:
        """Aplica material holográfico ciano semitransparente."""
        if self.lib:
            mat = self.lib.holograma(cor=LORENA_COLOR, opacidade=LORENA_OPACITY)
        else:
            # Fallback manual se MaterialLibrary não disponível
            mat = bpy.data.materials.new(f"Mat_{self.nome}_Holo")
            mat.use_nodes = True
            mat.blend_method = 'BLEND'
            nodes = mat.node_tree.nodes
            nodes.clear()

            emission = nodes.new('ShaderNodeEmission')
            emission.inputs['Color'].default_value = (*LORENA_COLOR, 1.0)
            emission.inputs['Strength'].default_value = 2.5

            transparent = nodes.new('ShaderNodeBsdfTransparent')
            mix = nodes.new('ShaderNodeMixShader')
            mix.inputs['Fac'].default_value = LORENA_OPACITY

            output = nodes.new('ShaderNodeOutputMaterial')
            links = mat.node_tree.links
            links.new(transparent.outputs['BSDF'], mix.inputs[1])
            links.new(emission.outputs['Emission'], mix.inputs[2])
            links.new(mix.outputs['Shader'], output.inputs['Surface'])

        self.mesh_obj.data.materials.clear()
        self.mesh_obj.data.materials.append(mat)
        self.material = mat
        print("   🎨 Material holográfico aplicado")

    # ──────────────────── ANIMAÇÕES IDLE ─────────────────────────────────────

    def apply_idle_animations(self) -> None:
        """Aplica animações de fundo: flutuar + respirar + piscar automático."""
        if not self.anim or not self.mesh_obj:
            print("⚠️ AnimationEngine não disponível.")
            return

        print("🎬 Aplicando animações idle...")
        self.anim.flutuar(self.mesh_obj, amplitude=0.04, velocidade=0.8)
        self.anim.respiracao(self.mesh_obj, amplitude_escala=0.008, velocidade=0.4)
        self._setup_blink_procedural()
        print("   ✅ Idle animations ativas (flutuar + respirar + piscar)")

    def _setup_blink_procedural(self, intervalo_frames=72) -> None:
        """Anima piscada a cada `intervalo_frames` frames."""
        if not self.mesh_obj or not self.mesh_obj.data.shape_keys:
            return

        blink_key = self.mesh_obj.data.shape_keys.key_blocks.get("blink")
        if not blink_key:
            return

        scene = bpy.context.scene
        total = scene.frame_end
        frame = 1

        while frame < total:
            # Olho aberto
            scene.frame_set(frame)
            blink_key.value = 0.0
            blink_key.keyframe_insert(data_path="value")

            # Piscar fechado
            scene.frame_set(frame + 2)
            blink_key.value = 1.0
            blink_key.keyframe_insert(data_path="value")

            # Olho aberto novamente
            scene.frame_set(frame + 4)
            blink_key.value = 0.0
            blink_key.keyframe_insert(data_path="value")

            frame += intervalo_frames

        # Interpolação LINEAR para piscada rápida
        if self.mesh_obj.data.shape_keys.animation_data:
            for fc in self.mesh_obj.data.shape_keys.animation_data.action.fcurves:
                if 'blink' in (fc.data_path or ''):
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'LINEAR'

    # ──────────────────── LIP SYNC ───────────────────────────────────────────

    def lip_sync(self, audio_path: str, step_frames: int = 3) -> None:
        """
        Sincronização labial procedural a partir de arquivo WAV.
        
        Modo simples: analisa energia do áudio a cada `step_frames` para
        abrir/fechar a boca proporcionalmente.
        
        Para sincronização precisa use Rhubarb:
            `lip_sync_from_rhubarb("arquivo.tsv")`
        
        Args:
            audio_path:   Caminho para arquivo .WAV 16-bit mono
            step_frames:  Intervalo de análise (3 = suave, 1 = preciso mas pesado)
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            print(f"❌ Áudio não encontrado: {audio_path}")
            return

        if not self.mesh_obj or not self.mesh_obj.data.shape_keys:
            print("❌ Mesh ou shape keys não encontradas. Execute build() primeiro.")
            return

        print(f"🔊 Lendo áudio: {audio_path.name}...")

        try:
            samples, framerate = self._read_wav(audio_path)
        except Exception as e:
            print(f"❌ Erro ao ler WAV: {e}")
            return

        scene = bpy.context.scene
        samples_per_frame = framerate / LORENA_FPS

        mouth_open_key = self.mesh_obj.data.shape_keys.key_blocks.get("mouth_open")
        mouth_ah_key   = self.mesh_obj.data.shape_keys.key_blocks.get("mouth_ah")
        mouth_closed_key = self.mesh_obj.data.shape_keys.key_blocks.get("mouth_closed")

        if not mouth_open_key:
            print("❌ Shape key 'mouth_open' não encontrada.")
            return

        total_frames = int(len(samples) / samples_per_frame)
        print(f"   {total_frames} frames | {framerate}Hz | step={step_frames}")

        for frame in range(1, total_frames, step_frames):
            scene.frame_set(frame)
            sample_start = int((frame - 1) * samples_per_frame)
            sample_end   = int(sample_start + samples_per_frame * step_frames)
            chunk = samples[sample_start:sample_end]

            if not chunk:
                continue

            # Energia RMS do chunk
            rms = math.sqrt(sum(s*s for s in chunk) / len(chunk))
            normalized = min(1.0, rms * 8.0)  # Amplifica e limita a 1.0

            # Aplica nas shape keys
            mouth_open_val = normalized * 0.9
            mouth_ah_val   = normalized * 0.7 if normalized > 0.4 else 0.0
            closed_val     = max(0.0, 0.8 - normalized * 1.5)

            mouth_open_key.value = mouth_open_val
            mouth_open_key.keyframe_insert(data_path="value")

            if mouth_ah_key:
                mouth_ah_key.value = mouth_ah_val
                mouth_ah_key.keyframe_insert(data_path="value")

            if mouth_closed_key:
                mouth_closed_key.value = closed_val
                mouth_closed_key.keyframe_insert(data_path="value")

        # Suaviza com BEZIER
        if self.mesh_obj.data.shape_keys.animation_data:
            action = self.mesh_obj.data.shape_keys.animation_data.action
            if action:
                for fc in action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'BEZIER'

        print(f"✅ Lip Sync concluído! {total_frames // step_frames} keyframes inseridos.")

    def lip_sync_from_rhubarb(self, tsv_path: str) -> None:
        """
        Sincronização labial precisa usando output TSV do Rhubarb.
        
        Formato TSV do Rhubarb:
            0.00    X
            0.12    B
            0.25    A
            ...
        
        Args:
            tsv_path: Caminho para arquivo .tsv gerado pelo Rhubarb
        """
        tsv_path = Path(tsv_path)
        if not tsv_path.exists():
            print(f"❌ TSV Rhubarb não encontrado: {tsv_path}")
            return

        if not self.mesh_obj or not self.mesh_obj.data.shape_keys:
            print("❌ Execute build() primeiro.")
            return

        print(f"📋 Lendo Rhubarb TSV: {tsv_path.name}...")

        # Parse do TSV
        cues = []
        with open(tsv_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    time_sec = float(parts[0])
                    phoneme  = parts[1].strip()
                    cues.append((time_sec, phoneme))

        if not cues:
            print("❌ Nenhum cue encontrado no TSV.")
            return

        scene = bpy.context.scene
        shape_keys = self.mesh_obj.data.shape_keys.key_blocks

        # Reset todas as shape keys a 0 no frame 1
        scene.frame_set(1)
        for sk_name in SHAPE_KEYS:
            sk = shape_keys.get(sk_name)
            if sk:
                sk.value = 0.0
                sk.keyframe_insert(data_path="value")

        for i, (time_sec, phoneme) in enumerate(cues):
            frame = int(time_sec * LORENA_FPS) + 1

            # Reset rápido antes do cue
            reset_frame = max(1, frame - 1)
            scene.frame_set(reset_frame)
            for sk_name in SHAPE_KEYS:
                sk = shape_keys.get(sk_name)
                if sk:
                    sk.value = 0.0
                    sk.keyframe_insert(data_path="value")

            # Aplica viseme mapeado
            scene.frame_set(frame)
            viseme_values = RHUBARB_VISEME_MAP.get(phoneme, {"mouth_closed": 0.5})
            for sk_name, val in viseme_values.items():
                sk = shape_keys.get(sk_name)
                if sk:
                    sk.value = val
                    sk.keyframe_insert(data_path="value")

        # Suaviza com BEZIER
        if self.mesh_obj.data.shape_keys.animation_data:
            action = self.mesh_obj.data.shape_keys.animation_data.action
            if action:
                for fc in action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'BEZIER'

        print(f"✅ Rhubarb Lip Sync: {len(cues)} cues aplicados.")

    # ──────────────────── UTILITÁRIOS ────────────────────────────────────────

    def _read_wav(self, path: Path) -> tuple:
        """Lê arquivo WAV e retorna (samples_float, framerate)."""
        with wave.open(str(path), 'rb') as wf:
            n_channels = wf.getnchannels()
            n_frames   = wf.getnframes()
            framerate  = wf.getframerate()
            sampwidth  = wf.getsampwidth()
            raw_data   = wf.readframes(n_frames)

        fmt = {1: 'b', 2: 'h', 4: 'i'}.get(sampwidth, 'h')
        total_samples = n_frames * n_channels
        samples = struct.unpack(f'<{total_samples}{fmt}', raw_data)

        # Mono (média se estéreo)
        if n_channels == 2:
            samples = [(samples[i] + samples[i+1]) / 2 for i in range(0, len(samples), 2)]

        max_val = float(2 ** (sampwidth * 8 - 1))
        samples_float = [s / max_val for s in samples]

        return samples_float, framerate

    def set_expression(self, expressao: str, intensidade: float = 1.0, frame: int = None) -> None:
        """
        Aplica uma expressão facial ao avatar.
        
        Args:
            expressao:   Nome da shape key ("smile", "angry", "surprise")
            intensidade: 0.0 a 1.0
            frame:       Se None, aplica sem keyframe
        """
        if not self.mesh_obj or not self.mesh_obj.data.shape_keys:
            return

        sk = self.mesh_obj.data.shape_keys.key_blocks.get(expressao)
        if not sk:
            print(f"⚠️ Expressão '{expressao}' não encontrada.")
            return

        sk.value = max(0.0, min(1.0, intensidade))
        if frame is not None:
            bpy.context.scene.frame_set(frame)
            sk.keyframe_insert(data_path="value")

    def wave_hello(self, frame_inicio: int = 1) -> None:
        """Anima o braço direito para acenar (saudação)."""
        if not self.armature_obj:
            print("⚠️ Armature não disponível.")
            return

        scene = bpy.context.scene
        arm = self.armature_obj

        # Levanta braço direito
        bone = arm.pose.bones.get("R_upper_arm")
        if not bone:
            return

        scene.frame_set(frame_inicio)
        bone.rotation_euler = Euler((0, 0, 0))
        bone.keyframe_insert(data_path="rotation_euler")

        scene.frame_set(frame_inicio + 12)
        bone.rotation_euler = Euler((0, 0, math.radians(-90)))
        bone.keyframe_insert(data_path="rotation_euler")

        # Oscilação da mão
        for i in range(3):
            f = frame_inicio + 18 + (i * 8)
            scene.frame_set(f)
            bone.rotation_euler = Euler((0, math.radians(15 if i % 2 == 0 else -15), math.radians(-90)))
            bone.keyframe_insert(data_path="rotation_euler")

        # Baixa braço
        scene.frame_set(frame_inicio + 50)
        bone.rotation_euler = Euler((0, 0, 0))
        bone.keyframe_insert(data_path="rotation_euler")

        print("👋 Lorena acenando!")


# ─────────────────────────────────────────────────────────────────────────────
# TESTE RÁPIDO
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    lorena = LorenaAvatar(posicao=(0, 0, 0))
    lorena.build()
    lorena.apply_idle_animations()

    # Anima expressão de saudação
    lorena.set_expression("smile", intensidade=0.8, frame=1)
    lorena.wave_hello(frame_inicio=12)

    print("\n🌟 LORENA PRONTA PARA RENDER!")
    print(f"   Mesh: {lorena.mesh_obj.name}")
    print(f"   Rig:  {lorena.armature_obj.name}")
    print("\n   Para lip sync (exemplo):")
    print('   lorena.lip_sync("audio/raw/lorena_fala.wav")')
