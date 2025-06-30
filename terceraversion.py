import json
import random

def ver_mis_shows():
    try:
        archivo = open("usuarios.txt", "r", encoding="utf-8")
        encontrado = False
        linea = archivo.readline()
        while linea:
            if linea.strip():  # Solo procesar si no está vacía
                datos = linea.strip().split(';')
                if datos[0] == dni_usuario:
                    encontrado = True
                    print(f"\nDNI: {dni_usuario}")
                    print(f"Nombre: {datos[1]}")
                    print("Shows comprados y cantidad de entradas:")
                    shows = datos[2].strip().split(',')
                    for show in shows:
                        if show:  # Solo mostrar shows no vacíos
                            partes = show.split("-")
                            if len(partes) == 4:
                                artista, fecha, sector, cantidad = partes
                                print(f"- {artista} | Fecha: {fecha} | Sector: {sector} | Entradas: {cantidad}")
                            else:
                                print(f"- (formato inválido): {show}")
                    break  # Salir del bucle una vez encontrado
            linea = archivo.readline()

        if not encontrado:
            print("No se encontraron shows para este DNI.")
    except FileNotFoundError:
        print("El archivo usuarios.txt no existe.")
    finally:
        archivo.close()
        
def cancelar_mis_shows(dni_usuario, eventos):
    try:
        archivo = open("usuarios.txt", "rt", encoding="utf-8")
        lineas = []
        linea = archivo.readline()
        while linea:
            lineas.append(linea)
            linea = archivo.readline()
        archivo.close()

        entradas_usuario = []
        for linea in lineas:
            partes = linea.strip().split(";")
            if partes[0] == dni_usuario:
                nombre = partes[1]
                entradas_usuario = partes[2].split(",") if len(partes) > 2 else []
                break

        if not entradas_usuario or entradas_usuario == [""]:
            print("No tenés entradas registradas para cancelar.")
            return

        print("Tus entradas:")
        for i, entrada in enumerate(entradas_usuario):
            print(f"{i+1}. {entrada}")

        opcion = int(input("¿Cuál entrada querés cancelar? (Número): ")) - 1

        if 0 <= opcion < len(entradas_usuario):
            entrada = entradas_usuario[opcion]
            partes_entrada = entrada.split("-")
            if len(partes_entrada) != 4:
                print("Entrada mal formada. No se puede cancelar.")
                return

            artista, fecha, sector, cantidad = partes_entrada
            cantidad = int(cantidad)

            print(f"Seleccionaste: {artista}-{fecha}-{sector}-{cantidad}")
            cantidad_cancelar = int(input(f"¿Cuántas de las {cantidad} querés cancelar?: "))
            while cantidad_cancelar < 1 or cantidad_cancelar > cantidad:
                print("Cantidad inválida.")
                cantidad_cancelar = int(input(f"¿Cuántas de las {cantidad} querés cancelar?: "))

            # Devolver entradas al stock
            for evento in eventos.values():
                if evento['Artista'] == artista and fecha in evento['Fechas'] and sector in evento['Fechas'][fecha]:
                    evento['Fechas'][fecha][sector]['Disponibilidad'] += cantidad_cancelar
                    break

            # Actualizar lista del usuario
            if cantidad_cancelar == cantidad:
                entradas_usuario.pop(opcion)
            else:
                nueva_entrada = f"{artista}-{fecha}-{sector}-{cantidad - cantidad_cancelar}"
                entradas_usuario[opcion] = nueva_entrada

            # Reescribir archivo
            archivo = open("usuarios.txt", "wt", encoding="utf-8")
            for linea in lineas:
                partes = linea.strip().split(";")
                if partes[0] == dni_usuario:
                    nueva_linea = f"{partes[0]};{partes[1]};{','.join(entradas_usuario)}\n"
                    archivo.write(nueva_linea)
                else:
                    archivo.write(linea)
            archivo.close()

            guardar_eventos(eventos)

            print("Entradas canceladas correctamente.")
            if not entradas_usuario:
                print("Ya no tenés más entradas registradas.")
        else:
            print("Opción inválida.")
    except Exception as e:
        print("Error al cancelar entrada:", e)







def cargar_eventos():
    """Carga los eventos desde el archivo JSON y los devuelve en la estructura de lista."""
    try:
        archivo = open('Eventos.json', 'rt', encoding='utf-8')
        eventos_json = json.load(archivo)
        

        return eventos_json;

    except FileNotFoundError:
        print("Archivo Eventos.json no encontrado. Se crea lista vacía.")
        return []
    except json.JSONDecodeError:
        print("Error al leer JSON. Verifica el formato.")
        return []
    finally:
        archivo.close()
    
# Cargamos los eventos al inicio para trabajar con ellos
eventos = cargar_eventos()

dni = ""

def creacion_usuario():
    global dni_usuario  
    nombre = input("Ingrese su nombre: ")
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Ingrese su nombre: ")
    dni_usuario = input("Ingrese su DNI: ")
    while not (dni_usuario.isdigit() and len(dni_usuario) == 8):
        print("DNI no válido. Debe tener 8 dígitos y ser solo números.")
        dni_usuario = input("Ingrese su DNI: ")
    print(len(dni_usuario))

    try: 
        entrada = open('usuarios.txt', 'rt', encoding='utf-8')
        linea = entrada.readline()
        while linea:
            linea = linea.strip()
            if linea:
                partes = linea.split(';')
                if len(partes) >= 2:
                    dni_existente = partes[0]
                    while dni_existente == dni_usuario:
                        print("El DNI ya está registrado. Por favor, ingrese otro.")
                        dni_usuario = input("Ingrese su DNI: ")
                else:
                    print("Línea mal formada:", linea)
            else:
                print("Línea mal formada:", linea)
            linea = entrada.readline()
    except FileNotFoundError:
        print("Error, archivo no encontrado.")
    finally:
        entrada.close()

    try: 
        archivo = open('usuarios.txt', 'a', encoding='utf-8')
        archivo.write(dni_usuario + ';' + nombre + ';' + '' + '\n')
        print(f"Usuario {nombre} creado exitosamente.")
        print("Bienvenido", nombre)
    except IOError:
        print("Error al escribir en el archivo usuarios.txt.")
    finally:
        archivo.close()


def ingreso_usuario():
    input_dni = input("Ingrese su DNI: ")
    while len(input_dni) != 8:
        print("DNI no válido. Debe tener 8 dígitos.")
        input_dni = input("Ingrese su DNI: ")

    try:
        archivo = open('usuarios.txt', 'rt', encoding='utf-8')
        linea = archivo.readline()
        while linea:
            linea = linea.strip()
            if linea:
                dni, nombre_apellido, eventos = linea.split(';')
                if dni == input_dni:
                    print()
                    print()
                    print(f"Bienvenido {nombre_apellido}")
                    return True, input_dni
            else:
                print("Línea mal formada:", linea)
            linea = archivo.readline()
        return False, input_dni  # DNI no encontrado
    except FileNotFoundError:
        print("El archivo usuarios.txt no existe.")
        return False, ""
    finally:
        try:
            archivo.close()
        except:
            pass 
            

def cargar_eventos():
    """Carga los eventos desde el archivo JSON y los devuelve en la estructura de lista."""
    try:
        archivo = open('Eventos.json', 'rt', encoding='utf-8')
        eventos_json = json.load(archivo)
        

        lista_eventos = []
        i = 1
        while str(i) in eventos_json:
            evento = eventos_json[str(i)]
            # Construimos la estructura de lista que usas para cada evento
            nuevo_evento = [
                evento['Artista'],          # nombre artista
                evento['Fechas'],           # lista fechas
                [evento['Sectores']['Campo']['Precio'], evento['Sectores']['Campo']['Disponibilidad']],
                [evento['Sectores']['Platea Alta']['Precio'], evento['Sectores']['Platea Alta']['Disponibilidad']],
                [evento['Sectores']['Platea Baja']['Precio'], evento['Sectores']['Platea Baja']['Disponibilidad']]
            ]
            lista_eventos.append(nuevo_evento)
            i += 1
        return lista_eventos

    except FileNotFoundError:
        print("Archivo Eventos.json no encontrado. Se crea lista vacía.")
        return []
    except json.JSONDecodeError:
        print("Error al leer JSON. Verifica el formato.")
        return []
    finally:
        archivo.close()

def guardar_eventos(eventos):
    """Guarda toda la estructura de eventos (tipo diccionario) en el archivo JSON."""
    try:
        archivo = open('Eventos.json', 'wt', encoding='utf-8')
        json.dump(eventos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")
    finally:
        archivo.close()



def nombre_sector(opcion_sector):
    if opcion_sector == 1:
        opcion_sector_diccionario = 'Campo'
    elif opcion_sector == 2:
        opcion_sector_diccionario = 'Platea Alta'
    elif opcion_sector == 3:
        opcion_sector_diccionario = 'Platea Baja'
    else:
        print("Opción no válida.")
        return None

    return opcion_sector_diccionario


def comprobar_disponibilidad(artista, opcion_sector):
    """
    Verifica si en un sector del artista hay entradas disponibles.
    artista: índice 1-based del artista en la lista eventos
    opcion_sector: 1=Campo, 2=Platea Alta, 3=Platea Baja
    """
    if opcion_sector in [1, 2, 3]:
        opcion_sector_diccionario = nombre_sector(opcion_sector)
        return eventos[str(artista)]["Sectores"][opcion_sector_diccionario]["Disponibilidad"] > 0
    return False

def seleccionar_artistas(eventos):
    """
    Muestra la lista de eventos con una opción 0 para volver.
    Devuelve el ID del evento elegido, o None si el usuario elige volver.
    """
    while True:
        print("Seleccione el evento (0 para volver):")
        for key, info in eventos.items():
            fechas = ', '.join(info['Fechas'].keys())
            print(f"{key}: {info['Artista']} — Fechas: {fechas} — {info['Sede']}")
        print("0: Volver")

        opcion = input("Ingrese el número del evento: ")
        if opcion == "0":
            return None
        if opcion in eventos:
            return int(opcion)
        print("Opción inválida. Intente nuevamente.")




"""def ver_fechas_del_artista(artista):
    Devuelve la lista de fechas disponibles para un artista.
    i = 1
    print(f"Fechas disponibles para {eventos[str(artista)]['Artista']}:")
    for fecha in eventos[str(artista)]["Fechas"]:
        print(f"{i}: {fecha}")
        i += 1
    
    return eventos[str(artista)]["Fechas"]"""

def seleccionar_sector(artista_id, fecha):
    """
    Muestra los sectores disponibles para una fecha específica de un evento.
    Devuelve el número de sector seleccionado si hay disponibilidad, o False.
    """
    print("Seleccione el sector:")
    print("1. Campo")
    print("2. Platea Alta")
    print("3. Platea Baja")

    opcion = int(input("Ingrese el número del sector: "))
    while opcion not in [1, 2, 3]:
        print("Opción no válida.")
        opcion = int(input("Ingrese el número del sector: "))

    sector_nombre = nombre_sector(opcion)
    disponibilidad = eventos[str(artista_id)]["Fechas"][fecha][sector_nombre]["Disponibilidad"]

    if disponibilidad > 0:
        precio = eventos[str(artista_id)]["Fechas"][fecha][sector_nombre]["Precio"]
        print(f"✅ Sector {sector_nombre} tiene {disponibilidad} entradas disponibles.")
        print(f"💵 Precio: ${precio}")
        return opcion
    else:
        print(f"❌ El sector {sector_nombre} no tiene disponibilidad.")
        return False


def modificar_precio():
    """Permite modificar el precio de un sector para una fecha específica de un evento."""
    print("---------------------------")
    print("Seleccione el evento:")
    evento_id = seleccionar_artistas(eventos)
    evento = eventos[str(evento_id)]

    fechas_disponibles = list(evento["Fechas"].keys())
    print(f"Fechas disponibles para {evento['Artista']} en {evento['Sede']}:")
    for i, fecha in enumerate(fechas_disponibles, 1):
        print(f"{i}. {fecha}")

    if not fechas_disponibles:
        print("Este evento no tiene fechas disponibles.")
        return

    indice_fecha = int(input("Seleccione la fecha (número): "))
    while indice_fecha < 1 or indice_fecha > len(fechas_disponibles):
        print("Opción inválida.")
        indice_fecha = int(input("Seleccione la fecha (número): "))
    fecha_elegida = fechas_disponibles[indice_fecha - 1]

    print("Seleccione el sector a modificar:")
    print("1. Campo")
    print("2. Platea Alta")
    print("3. Platea Baja")
    opcion = int(input("Opción: "))
    while opcion not in [1, 2, 3]:
        print("Opción inválida.")
        opcion = int(input("Opción: "))

    sector = nombre_sector(opcion)

    nuevo_precio = int(input(f"Ingrese el nuevo precio para el sector {sector}: "))
    while nuevo_precio <= 0:
        print("El precio debe ser un número positivo.")
        nuevo_precio = int(input(f"Ingrese el nuevo precio para el sector {sector}: "))

    evento["Fechas"][fecha_elegida][sector]["Precio"] = nuevo_precio
    guardar_eventos(eventos)

    print(f"✅ Precio actualizado: {sector} ahora cuesta ${nuevo_precio} para el evento del {fecha_elegida}.")




def agregar_artistas(nombre, fechas, disp_campo, precio_campo, disp_platea_alta, precio_platea_alta, disp_platea_baja, precio_platea_baja):
    """Agrega un artista nuevo y guarda en el JSON."""
    nuevo_artista = {
		'Artista': nombre,
            'Fechas': fechas,
			'Sectores': {
				'Campo': {
					'Precio': precio_campo,
					'Disponibilidad': disp_campo
				},
				'Platea Alta': {
					'Precio': precio_platea_alta,
					'Disponibilidad': disp_platea_alta
				},
				'Platea Baja': {
					'Precio': precio_platea_baja,
					'Disponibilidad': disp_platea_baja
				}
			}
	}
	# Obtener el último índice de los artistas en el diccionario
    if eventos:
        ultimo_indice = max(map(lambda x: int(x), eventos.keys()))
    else:
        ultimo_indice = 0

    # Agregar el nuevo artista con el siguiente índice
    eventos[str(ultimo_indice + 1)] = nuevo_artista
    guardar_eventos(eventos)

def modificar_disponibilidad():
    """Permite modificar la disponibilidad de un sector en una fecha específica de un evento."""
    print("---------------------------")
    print("Seleccione el evento:")
    evento_id = seleccionar_artistas(eventos)
    evento = eventos[str(evento_id)]
    
    # 1) Validar que haya fechas
    fechas = list(evento["Fechas"].keys())
    if not fechas:
        print("❌ No hay fechas cargadas para este evento.")
        return

    # 2) Listar y seleccionar fecha
    print(f"Fechas disponibles para {evento['Artista']}:")
    for i, fecha in enumerate(fechas, 1):
        print(f"{i}. {fecha}")
    while True:
        sel = input("Seleccione la fecha (número): ")
        if sel.isdigit() and 1 <= (idx := int(sel)) <= len(fechas):
            fecha_elegida = fechas[idx - 1]
            break
        print("❌ Entrada inválida. Intente de nuevo.")

    # 3) Listar sectores con marca si están dados de baja
    sectores = evento["Fechas"][fecha_elegida]
    nombres = list(sectores.keys())
    print("Sectores:")
    for i, nombre in enumerate(nombres, 1):
        dispo = sectores[nombre]["Disponibilidad"]
        tag = " (dado de baja)" if dispo == 0 else ""
        print(f"{i}. {nombre}{tag} — {dispo} disponibles")

    # 4) Seleccionar sector
    while True:
        sel = input("Seleccione el número del sector a modificar: ")
        if sel.isdigit() and 1 <= (idx := int(sel)) <= len(nombres):
            sector_seleccionado = nombres[idx - 1]
            break
        print("❌ Entrada inválida. Intente de nuevo.")

    # 5) Ingresar nueva disponibilidad
    while True:
        nuevo = input(f"Ingrese la nueva disponibilidad para {sector_seleccionado}: ")
        if nuevo.isdigit() and int(nuevo) >= 0:
            nueva_disponibilidad = int(nuevo)
            break
        print("❌ Debe ser un número entero ≥ 0.")

    # 6) Confirmar cambio
    confirm = input(f"Confirma cambiar disponibilidad de {sector_seleccionado} en {fecha_elegida} a {nueva_disponibilidad}? (s/n): ").lower()
    if confirm != 's':
        print("Operación cancelada.")
        return

    # 7) Aplicar y guardar
    evento["Fechas"][fecha_elegida][sector_seleccionado]["Disponibilidad"] = nueva_disponibilidad
    guardar_eventos(eventos)
    print(f"✅ Disponibilidad actualizada: {nueva_disponibilidad} lugares disponibles en {sector_seleccionado} para el evento del {fecha_elegida}.")






def bajar_fecha():
    """Permite eliminar una fecha de un evento específico."""
    print("---------------------------")
    print("Seleccione el evento del cual desea bajar una fecha:")
    evento_id = seleccionar_artistas(eventos)
    id_evento = str(evento_id)
    evento = eventos[id_evento]
    artista = evento["Artista"]

    fechas_disponibles = list(evento["Fechas"].keys())
    if not fechas_disponibles:
        print("Este evento no tiene fechas cargadas.")
        return

    print(f"Fechas disponibles para {artista}:")
    for i, fecha in enumerate(fechas_disponibles, 1):
        print(f"{i}: {fecha}")

    # ✅ Validación de entrada
    entrada_valida = False
    while not entrada_valida:
        seleccion = input("Seleccione el número de la fecha a eliminar: ")
        if seleccion.isdigit():
            indice = int(seleccion)
            if 1 <= indice <= len(fechas_disponibles):
                entrada_valida = True
            else:
                print("Número fuera de rango. Intente de nuevo.")
        else:
            print("Ingrese un número válido del listado.")

    fecha_a_borrar = fechas_disponibles[indice - 1]
    confirmacion = input(f"¿Está seguro que desea eliminar la fecha {fecha_a_borrar}? (s/n): ").lower()

    if confirmacion == 's':
        del evento["Fechas"][fecha_a_borrar]
        guardar_eventos(eventos)
        print("📆 Fecha eliminada con éxito.")
    else:
        print("Operación cancelada.")


def baja_evento():
    """Da de baja un evento completo (artista + sede + todas sus fechas)."""
    print("---------------------------")
    print("Seleccione el evento que desea eliminar (0 para volver):")
    # Listamos todos los eventos con su ID
    for key, info in eventos.items():
        artista = info["Artista"]
        sede    = info.get("Sede", "—")
        fechas  = ", ".join(info["Fechas"].keys()) or "Sin fechas"
        print(f"{key}: {artista} — {sede} — Fechas: {fechas}")
    print("0: Volver")

    seleccion = input("Ingrese el número del evento: ").strip()
    if seleccion == "0":
        return

    if seleccion not in eventos:
        print("❌ Opción inválida.")
        return

    evento = eventos[seleccion]
    artista = evento["Artista"]
    sede    = evento.get("Sede", "—")
    fechas  = ", ".join(evento["Fechas"].keys()) or "Sin fechas"

    print(f"\n⚠️ Vas a eliminar este evento:")
    print(f"   {seleccion}: {artista} — {sede} — Fechas: {fechas}")
    confirm = input("¿Confirma la baja? (s/n): ").strip().lower()
    if confirm == 's':
        del eventos[seleccion]
        guardar_eventos(eventos)
        print("✅ Evento eliminado con éxito.")
    else:
        print("Operación cancelada.")




def bajar_sector():
    """Da de baja (pone en 0 la disponibilidad) un sector de una fecha específica de un evento."""
    print("---------------------------")
    print("Seleccione el evento donde desea dar de baja un sector:")
    evento_id = seleccionar_artistas(eventos)
    if evento_id is None:
        return
    evento = eventos[str(evento_id)]
    artista = evento["Artista"]

    fechas = list(evento["Fechas"].keys())
    if not fechas:
        print("❌ Este evento no tiene fechas disponibles.")
        return

    # Selección de fecha con opción de volver
    while True:
        print(f"\nFechas disponibles para {artista}:")
        for i, f in enumerate(fechas, 1):
            print(f"{i}. {f}")
        print("0. Volver")
        sel = input("Seleccione el número de la fecha: ")
        if sel == "0":
            return
        if sel.isdigit() and 1 <= int(sel) <= len(fechas):
            fecha_elegida = fechas[int(sel) - 1]
            break
        print("❌ Opción inválida. Intente de nuevo.")

    sectores = evento["Fechas"][fecha_elegida]
    nombres = list(sectores.keys())

    # Selección de sector con indicador de baja y opción de volver
    while True:
        print(f"\nSectores para {fecha_elegida}:")
        for i, nombre in enumerate(nombres, 1):
            dispo = sectores[nombre]["Disponibilidad"]
            tag = " (dado de baja)" if dispo == 0 else ""
            print(f"{i}. {nombre}{tag}")
        print("0. Volver")
        sel2 = input("Seleccione el número del sector a dar de baja: ")
        if sel2 == "0":
            return
        if sel2.isdigit() and 1 <= int(sel2) <= len(nombres):
            sector_sel = nombres[int(sel2) - 1]
            break
        print("❌ Opción inválida. Intente de nuevo.")

    # Si ya estaba dado de baja
    if sectores[sector_sel]["Disponibilidad"] == 0:
        print(f"⚠️ El sector '{sector_sel}' ya se encuentra dado de baja.")
        return

    # Confirmación y baja
    confirm = input(f"¿Seguro que desea dar de baja el sector '{sector_sel}' en la fecha {fecha_elegida}? (s/n): ").strip().lower()
    if confirm == 's':
        sectores[sector_sel]["Disponibilidad"] = 0
        guardar_eventos(eventos)
        print(f"❌ Sector '{sector_sel}' dado de baja correctamente para la fecha {fecha_elegida}.")
    else:
        print("Operación cancelada.")





def agregar_fecha():
    """Agrega una nueva fecha con sectores y disponibilidad a un evento específico."""
    print("---------------------------")
    print("Seleccione el evento al que desea agregar una fecha:")
    evento_id = seleccionar_artistas(eventos)
    evento = eventos[str(evento_id)]
    artista_nombre = evento["Artista"]

    nueva_fecha = input(f"Ingrese la nueva fecha para {artista_nombre} (formato dd/mm/aa): ").strip()
    while not es_fecha_valida(nueva_fecha):
        print("Fecha no válida. Debe estar en formato dd/mm/aa y ser una fecha real.")
        nueva_fecha = input("Ingrese la nueva fecha: ").strip()

    # Verificar si la fecha ya existe
    if nueva_fecha in evento["Fechas"]:
        print("Esa fecha ya está registrada para este evento.")
        return

    # Ingreso de sectores
    sectores = {}
    for nombre_sector in ["Campo", "Platea Alta", "Platea Baja"]:
        precio = int(input(f"Ingrese el precio para {nombre_sector}: "))
        while precio <= 0:
            print("El precio debe ser positivo.")
            precio = int(input(f"Ingrese el precio para {nombre_sector}: "))

        disponibilidad = int(input(f"Ingrese la disponibilidad para {nombre_sector}: "))
        while disponibilidad < 0:
            print("La disponibilidad no puede ser negativa.")
            disponibilidad = int(input(f"Ingrese la disponibilidad para {nombre_sector}: "))

        sectores[nombre_sector] = {
            "Precio": precio,
            "Disponibilidad": disponibilidad
        }

    # Agregar la nueva fecha con sectores
    evento["Fechas"][nueva_fecha] = sectores
    guardar_eventos(eventos)

    print(f"✅ Fecha {nueva_fecha} agregada con éxito al evento de {artista_nombre}.")




def ver_entradas_disponibles(evento_id):
    """Alias de ver_entradas_disponibles_por_fecha()."""
    ver_entradas_disponibles_por_fecha(evento_id)



	

def validar_opcion_menu(opciones_validas):
	"""Valida que la opción ingresada sea válida."""
	opcion = input("Seleccione una opción: ")
	while opcion not in opciones_validas:
		print("Opción no válida. Por favor, seleccione una opción del menú.")
		opcion = input("Seleccione una opción: ")
	return opcion

def procesar_opcion_usuario(opcion):
    """Procesa las opciones del usuario en el menú principal."""
    if opcion == "1":
        procesar_opcion_ver_artistas()
    elif opcion == "2":
        ver_mis_shows()
    elif opcion == "3":
        cancelar_mis_shows(dni_usuario, eventos)
    elif opcion == "9":
        ingresar_administrador()



def procesar_opcion_ver_artistas():
    """Procesa la opción de ver artistas y sus subopciones."""
    while True:
        eid = seleccionar_artistas(eventos)
        if eid is None:
            return                        # vuelve al menú principal

        evento = eventos[str(eid)]
        print(f"\nArtista elegido: {evento['Artista']}")
        print(f"Estadio: {evento['Sede']}")
        print("Fechas disponibles:")
        for f in evento["Fechas"].keys():
            print(f"  📅 {f}")
        print("---------------------------")
        print("[1] Proceder con la compra")
        print("[2] Ver entradas disponibles")
        print("[0] Volver")
        elec = validar_opcion_menu(["0","1","2"])
        if elec == "0":
            continue                      # vuelvo a elegir evento
        elif elec == "1":
            proceder_con_compra(eid)
        else:
            ver_entradas_disponibles_por_fecha(eid)
        return                            # tras acción vuelvo al menú principal


def proceder_con_compra(artista_id):
    """Permite al usuario proceder con la compra de entradas."""
    global dni_usuario
    evento = eventos[str(artista_id)]
    fechas = list(evento["Fechas"].keys())

    # --- Selección de fecha ---
    if len(fechas) == 1:
        # cuando sólo hay una fecha, nos ahorramos el listado
        fecha_seleccionada = fechas[0]
        print(f"🔹 Sólo hay una fecha: {fecha_seleccionada}")
    else:
        print("Seleccione la fecha:")
        for i, f in enumerate(fechas, 1):
            print(f"  {i}. {f}")
        idx = int(input("Fecha (0 para volver): "))
        if idx == 0:
            return  # volvemos al menú anterior
        while idx < 1 or idx > len(fechas):
            print("Opción inválida.")
            idx = int(input("Fecha (0 para volver): "))
            if idx == 0:
                return
        fecha_seleccionada = fechas[idx - 1]

    # --- Selección de sector ---
    print("\nSeleccione el sector (0 para volver):")
    print("  1. Campo")
    print("  2. Platea Alta")
    print("  3. Platea Baja")
    opcion_sector = int(input("Sector: "))
    if opcion_sector == 0:
        return
    while opcion_sector not in (1, 2, 3):
        print("Opción inválida.")
        opcion_sector = int(input("Sector (0 para volver): "))
        if opcion_sector == 0:
            return

    sector = nombre_sector(opcion_sector)
    info = evento["Fechas"][fecha_seleccionada][sector]
    dispo = info["Disponibilidad"]
    precio = info["Precio"]

    print(f"\nDisponibilidad: {dispo} entradas")
    print(f"Precio:     ${precio}")
    print("ℹ️ Límite: máximo 5 entradas por persona.")
    cantidad = int(input("Cantidad (0 para volver): "))
    if cantidad == 0:
        return
    while cantidad < 1 or cantidad > 5 or cantidad > dispo:
        print("Cantidad inválida. Debe ser 1–5 y no superar la disponibilidad.")
        cantidad = int(input("Cantidad (0 para volver): "))
        if cantidad == 0:
            return

    # --- Actualizar stock en JSON ---
    evento["Fechas"][fecha_seleccionada][sector]["Disponibilidad"] -= cantidad
    guardar_eventos(eventos)

    # --- Registrar la compra en usuarios.txt ---
    try:
        # Leemos todas las líneas
        with open("usuarios.txt", "rt", encoding="utf-8") as f:
            lines = f.readlines()

        out = []
        for line in lines:
            dni, nombre, shows_str = line.rstrip("\n").split(";", 2)
            if dni == dni_usuario:
                shows = shows_str.split(",") if shows_str else []
                # Buscamos un show existente mismo artista+fecha+sector
                found = False
                for i, s in enumerate(shows):
                    if s.startswith(f"{evento['Artista']}-{fecha_seleccionada}-{sector}"):
                        parts = s.split("-")
                        parts[3] = str(int(parts[3]) + cantidad)
                        shows[i] = "-".join(parts)
                        found = True
                        break
                if not found:
                    shows.append(f"{evento['Artista']}-{fecha_seleccionada}-{sector}-{cantidad}")
                out.append(f"{dni};{nombre};{','.join(shows)}\n")
            else:
                out.append(line)

        # Reescribimos todo el archivo
        with open("usuarios.txt", "wt", encoding="utf-8") as f:
            f.writelines(out)

    except Exception as e:
        print("Error al registrar la compra:", e)
        return

    total = cantidad * precio
    print(f"\n✅ Compra registrada. Total a pagar: ${total}")



def ver_fechas_disponibles(evento_id):
    """Muestra solo las fechas disponibles para un evento específico."""
    evento = eventos[str(evento_id)]
    print(f"\nFechas disponibles para {evento['Artista']} en {evento['Sede']}:\n")
    for i, fecha in enumerate(evento["Fechas"].keys(), 1):
        print(f"{i}. {fecha}")

def ver_todas_las_fechas_del_artista(nombre_artista):
    print(f"\nFechas disponibles para {nombre_artista}:")
    encontrado = False
    for evento in eventos.values():
        if evento["Artista"].lower() == nombre_artista.lower():
            for fecha in evento["Fechas"]:
                print(f"📅 {fecha} - {evento['Sede']}")
                encontrado = True
    if not encontrado:
        print("No se encontraron fechas para este artista.")
    print()

def ver_entradas_disponibles_por_fecha(evento_id):
    """Muestra las entradas disponibles para cada fecha y sector de un evento específico."""
    evento = eventos[str(evento_id)]
    print(f"\nEntradas disponibles para {evento['Artista']} en {evento['Sede']}:\n")

    for fecha, sectores in evento["Fechas"].items():
        print(f"📅 Fecha: {fecha}")
        for sector, info in sectores.items():
            print(f"  🪑 {sector}: {info['Disponibilidad']} entradas disponibles a ${info['Precio']}")
        print("---------------------------")




def ingresar_administrador():
	"""Permite el ingreso al menú de administrador."""
	print("Ingreso de administrador")
	print("---------------------------")
	usuario = input("Ingrese su usuario: ")
	contrasena = input("Ingrese su contraseña: ")
	if usuario == "admin" and contrasena == "admin":
		mostrar_menu_administrador()
	else:
		print("Usuario o contraseña incorrectos.")

def mostrar_menu_administrador():
    """Muestra el menú de administrador y procesa sus opciones."""
    opcion_administrador = ""
    while opcion_administrador != "0":
        print()
        print("Bienvenido Administrador")
        print("---------------------------")
        print("[1] Modificar precios")
        print("[2] Modificar disponibilidad")
        print("[3] Agregar artistas")
        print("[4] Ver Usuarios")
        print("[5] Baja fecha")
        print("[6] Baja sector")
        print("[7] Agregar fecha")
        print("[8] Baja evento")
        print("---------------------------")
        print("[0] Salir")
        print("---------------------------")
        opcion_administrador = validar_opcion_menu(
            ["1", "2", "3", "4", "5", "6", "7", "8", "0"]
        )

        if opcion_administrador == "1":
            modificar_precio()
        elif opcion_administrador == "2":
            modificar_disponibilidad()
        elif opcion_administrador == "3":
            agregar_nuevo_evento()
        elif opcion_administrador == "4":
            mostrar_usuarios()
        elif opcion_administrador == "5":
            bajar_fecha()
        elif opcion_administrador == "6":
            bajar_sector()
        elif opcion_administrador == "7":
            agregar_fecha()
        elif opcion_administrador == "8":
            baja_evento()


def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

def es_fecha_valida(fecha):
    partes = fecha.split('/')
    if len(partes) != 3:
        return False
    
    try:
        dia = int(partes[0])
        mes = int(partes[1])
        año = int(partes[2])

    except ValueError:
        return False
    
    if año < 1 or mes < 1 or mes > 12 or dia < 1:
        return False
    
    dias_por_mes = [31, 29 if es_bisiesto(año) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if dia > dias_por_mes[mes - 1]:
        return False
    
    return True


def agregar_nuevo_evento():
    """Permite agregar un nuevo evento con artista, fecha, sede, sectores y precios."""
    nombre = input("Ingrese el nombre del artista: ")
    while not nombre.strip():
        print("El nombre no puede estar vacío.")
        nombre = input("Ingrese el nombre del artista: ")

    fecha = input("Ingrese la fecha del evento (dd/mm/yy): ").strip()
    while not es_fecha_valida(fecha):
        print("Fecha inválida. Debe estar en formato dd/mm/yy y ser una fecha real.")
        fecha = input("Ingrese la fecha del evento (dd/mm/yy): ").strip()

    sede = input("Ingrese el nombre del estadio o sede: ").strip()
    while not sede:
        print("La sede no puede estar vacía.")
        sede = input("Ingrese el nombre del estadio o sede: ").strip()

    # Ingreso de sectores
    sectores = {}
    for nombre_sector in ["Campo", "Platea Alta", "Platea Baja"]:
        precio = int(input(f"Ingrese el precio para {nombre_sector}: "))
        while precio <= 0:
            print("El precio debe ser positivo.")
            precio = int(input(f"Ingrese el precio para {nombre_sector}: "))

        disponibilidad = int(input(f"Ingrese la disponibilidad para {nombre_sector}: "))
        while disponibilidad < 0:
            print("La disponibilidad no puede ser negativa.")
            disponibilidad = int(input(f"Ingrese la disponibilidad para {nombre_sector}: "))

        sectores[nombre_sector] = {
            "Precio": precio,
            "Disponibilidad": disponibilidad
        }

    # Crear evento con nueva estructura
    nuevo_evento = {
        "Artista": nombre,
        "Sede": sede,
        "Fechas": {
            fecha: sectores
        }
    }

    # Calcular nuevo índice
    nuevo_indice = str(max(map(int, eventos.keys())) + 1 if eventos else 1)
    eventos[nuevo_indice] = nuevo_evento
    guardar_eventos(eventos)

    print("✅ Evento agregado con éxito.")



def mostrar_usuarios():
    """Muestra los usuarios en forma de tabla desde usuarios.txt, con opción recursiva usando readline()."""

    def mostrar_recursivo_desde_lista(lineas, i):
        if i < 0:
            return
        linea = lineas[i].strip()
        if linea:
            try:
                dni, nombre_apellido, eventos = linea.split(';')
                print(f"{dni:<15}{nombre_apellido:<30}{eventos:<20}")
            except ValueError:
                print("Línea mal formada:", linea)
        mostrar_recursivo_desde_lista(lineas, i - 1)

    try:
        archivo = open('usuarios.txt', 'rt', encoding='utf-8')
        print("¿Desea ver los usuarios de abajo hacia arriba? (s/n)")
        respuesta = input().lower()

        print('Usuarios Registrados: ')
        print(f"{'DNI':<15}{'Nombre y Apellido':<30}{'Eventos':<20}")
        print(f"{'-'*15}{'-'*30}{'-'*20}")

        if respuesta == 's':
            lineas = []
            linea = archivo.readline()
            while linea:
                lineas.append(linea)
                linea = archivo.readline()
            # Mostrar recursivamente
            mostrar_recursivo_desde_lista(lineas, len(lineas) - 1)
        else:
            # Mostrar normalmente
            linea = archivo.readline()
            while linea:
                linea = linea.strip()
                if linea:
                    try:
                        dni, nombre_apellido, eventos = linea.split(';')
                        print(f"{dni:<15}{nombre_apellido:<30}{eventos:<20}")
                    except ValueError:
                        print("Línea mal formada:", linea)
                linea = archivo.readline()

    except FileNotFoundError:
        print("El archivo usuarios.txt no existe.")
    finally:
        archivo.close()
        
def opcion_de_ingreso():
    global dni_usuario  # <<--- también clave aquí
    opcion_inicio = validar_opcion_menu(["1", "2"])

    if opcion_inicio == "1":
        creacion_usuario()
    else:
        validacion = False
        dni_usuario = ""
        while not validacion:
            validacion, dni_usuario = ingreso_usuario()
            if validacion:
                break
            if not validacion and dni_usuario != "":	
                print("DNI no encontrado. Por favor, ingrese un DNI válido.")
    return dni_usuario


#PROGRAMA PRINCIPAL
def main():
	opcion = ""
	while opcion != "0":
		print()
		print("---------------------------")
		print("MENÚ DEL SISTEMA           ")
		print("---------------------------")
		print("[1] Ver artistas")
		print("[2] Ver mis shows")
		print("[3] Cancelar una entrada")
		print("[9] Ingresar Administrador")
		print("---------------------------")
		print("[0] Salir del programa")
		print()
		
		opcion = validar_opcion_menu(["0", "1", "2", "3", "9"])
		procesar_opcion_usuario(opcion)
	print("Gracias por usar el sistema de venta de entradas. ¡Hasta luego!")


def ver_dni():
    print('Tu dni es: ', dni_usuario)

def bienvenida():
    print("---------------------------")
    print("BIENVENIDO AL SISTEMA     ")
    print("---------------------------")
    print("[1] Crear usuario")
    print("[2] Ingresar con DNI")
    print("---------------------------")
	
    dni = opcion_de_ingreso()
    
    return dni
    
dni_usuario = bienvenida()
main()