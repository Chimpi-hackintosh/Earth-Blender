"""Earth-Blender | Cena estilizada da Terra para Blender 3.6+.

Autor: Chimpi-hackintosh
Execute no Blender: blender --background --python earth_blender.py -- --render
Sem --render, a cena é criada e salva em earth_scene.blend
"""
import argparse
import math
import sys
from pathlib import Path

import bpy

AUTHOR = "Chimpi-hackintosh"


def material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


def earth_material():
    mat = material("Terra | oceanos e continentes estilizados", (0.04, 0.23, 0.65), 0.72)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    tex = nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = 3.4
    tex.inputs["Detail"].default_value = 6.0
    tex.inputs["Roughness"].default_value = 0.65
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "LINEAR"
    cr = ramp.color_ramp
    cr.elements.remove(cr.elements[1])
    palette = [
        (0.00, (0.004, 0.018, 0.11, 1)), # mar profundo
        (0.40, (0.01, 0.16, 0.43, 1)),
        (0.53, (0.03, 0.43, 0.64, 1)),
        (0.56, (0.05, 0.27, 0.11, 1)), # terra
        (0.67, (0.12, 0.42, 0.14, 1)),
        (0.78, (0.56, 0.43, 0.24, 1)),
        (0.91, (0.94, 0.94, 0.88, 1)), # montanhas geladas
    ]
    for i, (pos, rgba) in enumerate(palette):
        el = cr.elements[0] if i == 0 else cr.elements.new(pos)
        el.position = pos
        el.color = rgba
    links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def cloud_material():
    mat = bpy.data.materials.new("Nuvens | procedurais")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    output = nodes.new("ShaderNodeOutputMaterial")
    mix = nodes.new("ShaderNodeMixShader")
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    cloud = nodes.new("ShaderNodeBsdfPrincipled")
    cloud.inputs["Base Color"].default_value = (0.92, 0.96, 1.0, 1)
    cloud.inputs["Roughness"].default_value = 1.0
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 8.0
    noise.inputs["Detail"].default_value = 5.0
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.58
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.72
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], mix.inputs[0])
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(cloud.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs["Surface"])
    return mat


def sphere(name, radius, mat, segments=128):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=64, radius=radius, location=(0, 0, 0)
    )
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(mat)
    return obj


def make_scene(resolution=960):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    planet = sphere("Earth | Chimpi-hackintosh", 2.0, earth_material())
    planet.rotation_euler = (math.radians(12), 0, math.radians(24))
    cloud = sphere("Cloud Layer", 2.025, cloud_material())
    cloud.rotation_euler = (0, math.radians(18), math.radians(-12))

    bpy.ops.object.camera_add(location=(0, -8.5, 3.2))
    camera = bpy.context.object
    camera.name = "Camera | Earth"
    direction = -camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 5.7
    bpy.context.scene.camera = camera

    bpy.ops.object.light_add(type="AREA", location=(-3.5, -4.5, 5.0))
    key = bpy.context.object
    key.name = "Sunlight | softbox"
    key.data.energy = 850
    key.data.shape = "DISK"
    key.data.size = 5.0

    world = bpy.data.worlds.new("Space") if not bpy.data.worlds else bpy.data.worlds[0]
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.003, 0.006, 0.017, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4

    scene = bpy.context.scene
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    # Cycles funciona em Blender 3.6+ sem depender do nome das versões do Eevee
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 32
    scene.render.filepath = str(Path.cwd() / "earth_render.png")
    return scene


def main():
    arguments = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Crie uma Terra 3D estilizada no Blender")
    parser.add_argument("--render", action="store_true", help="Renderizar PNG")
    parser.add_argument("--resolution", type=int, default=960, help="Tamanho em pixels (256-4096)")
    parser.add_argument("--output", default="earth_scene.blend", help="Caminho do arquivo .blend")
    args = parser.parse_args(arguments)
    if not 256 <= args.resolution <= 4096:
        parser.error("--resolution deve estar entre 256 e 4096")
    make_scene(args.resolution)
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print(f"Earth-Blender por {AUTHOR}: cena salva em {out}")
    if args.render:
        bpy.ops.render.render(write_still=True)
        print(f"Render salvo em {bpy.context.scene.render.filepath}")


if __name__ == "__main__":
    main()
