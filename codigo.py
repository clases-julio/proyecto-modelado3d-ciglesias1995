import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.ops.object.select_pattern(pattern=nombreObjeto, case_sensitive=False, extend=True) # ...excepto el buscado

def seleccionarVariosObjetos(lista_objetos): # Pasa lista de objetos y los selecciona
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    for nombreObjeto in lista_objetos:
        bpy.ops.object.select_pattern(pattern=nombreObjeto, case_sensitive=False, extend=True)

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.scene.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')

'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    # Creación de un cubo y transformaciones de este:
    borrarObjetos()
    #bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(3.14, 0, 0), scale=(1, 1, 1))
    #bpy.ops.view3d.camera_to_view()
    
    bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(8, 8, 1))
    Activo.renombrar("main_OVNI_body")
    bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0.832209), scale=(4, 4, 1))
    Activo.renombrar("upper_OVNI_body")
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(2, 2, 2))
    bpy.ops.transform.translate(value=(0, 0, 1.07601), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    Activo.renombrar("OVNI_windshield")
    seleccionarObjeto("main_OVNI_body")
    
    # Join both OVNI bodies
    body = []
    body.append("upper_OVNI_body")
    #body.append("main_OVNI_body")
    body.append("OVNI_windshield")
    seleccionarVariosObjetos(body)
    bpy.ops.object.join()

    
    # MOTORS
    # Definimos primer cilidro hueco del motor
    bpy.ops.mesh.primitive_cylinder_add(end_fill_type='NOTHING', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = 0.09 # grosor 0.09


    Activo.renombrar("main_motor_body")
    Seleccionado.rotarX(1.57079)
  
    # Ponemos la "tapa" al motor
    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 0.05))
    Activo.renombrar("motor_tape")
    Seleccionado.rotarX(1.57079)
    bpy.ops.transform.translate(value=(0, 1.02379, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

    # Unimos ambos cilidros
    motor_body = []
    motor_body.append("motor_tape")
    motor_body.append("main_motor_body")
    seleccionarVariosObjetos(motor_body)
    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(-7.79881, -1.0697, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)



    # Reactor
    bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    Activo.renombrar("reactor")
    bpy.ops.transform.translate(value=(0, 1.02379, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

    bpy.context.object.rotation_euler[0] = -1.5708
    bpy.context.object.scale[0] = 0.5
    bpy.context.object.scale[1] = 0.5
    bpy.context.object.scale[2] = 2

    # Truncamos el cono 
    bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.bevel(offset=1.08926, offset_pct=0, affect='VERTICES')
    bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.primitive_cylinder_add(end_fill_type='NOTHING', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.5, 0.5, 0.1))
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    Seleccionado.rotarX(1.57079)
    bpy.context.object.modifiers["Solidify"].thickness = 0.09 # grosor 0.09
    bpy.ops.transform.translate(value=(-0, -1.06975, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    Activo.renombrar("output_reactor")
    motor_tot = []
    motor_tot.append("reactor")
    #motor_tot.append("motor_tape")
    motor_tot.append("output_reactor")
    seleccionarVariosObjetos(motor_tot)
 
    bpy.ops.object.join()
    seleccionarObjeto("output_reactor")
    bpy.ops.transform.translate(value=(-7.79881, -1.09452, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    










    # Definimos primer cilidro hueco del motor
    bpy.ops.mesh.primitive_cylinder_add(end_fill_type='NOTHING', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = 0.09 # grosor 0.09


    Activo.renombrar("main_motor_body2")
    Seleccionado.rotarX(1.57079)
  
    # Ponemos la "tapa" al motor
    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 0.05))
    Activo.renombrar("motor_tape2")
    Seleccionado.rotarX(1.57079)
    bpy.ops.transform.translate(value=(0, 1.02379, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

    # Unimos ambos cilidros
    motor_body = []
    motor_body.append("motor_tape2")
    motor_body.append("main_motor_body2")
    seleccionarVariosObjetos(motor_body)
    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(7.79881, -1.0697, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)



    # Reactor
    bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    Activo.renombrar("reactor2")
    bpy.ops.transform.translate(value=(0, 1.02379, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

    bpy.context.object.rotation_euler[0] = -1.5708
    bpy.context.object.scale[0] = 0.5
    bpy.context.object.scale[1] = 0.5
    bpy.context.object.scale[2] = 2

    # Truncamos el cono 
    bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.bevel(offset=1.08926, offset_pct=0, affect='VERTICES')
    bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.primitive_cylinder_add(end_fill_type='NOTHING', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.5, 0.5, 0.1))
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    Seleccionado.rotarX(1.57079)
    bpy.context.object.modifiers["Solidify"].thickness = 0.09 # grosor 0.09
    bpy.ops.transform.translate(value=(-0, -1.06975, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    Activo.renombrar("output_reactor2")
    motor_tot = []
    motor_tot.append("reactor2")
    #motor_tot.append("motor_tape")
    motor_tot.append("output_reactor2")
    seleccionarVariosObjetos(motor_tot)
 
    bpy.ops.object.join()
    seleccionarObjeto("output_reactor2")
    bpy.ops.transform.translate(value=(7.79881, -1.09452, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

