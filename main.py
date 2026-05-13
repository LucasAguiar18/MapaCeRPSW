# ==========================================================
# main.py
# CERPSW NAVIGATOR 3D - VERSION MEJORADA
# ==========================================================

import math
import networkx as nx

from panda3d.core import (
    AmbientLight,
    DirectionalLight,
    TransparencyAttrib,
    WindowProperties,
    Vec3,
)

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.OnscreenText import OnscreenText

# ==========================================================
# GRAFO AJUSTADO AL MAPA REAL
# ==========================================================

LOCATIONS = {

    # ENTRADA
    "Entrada principal": (1.5, 47, 0.2),
    "P.A3": (3, 47, 0.2),

    # PASILLO
    "Pasillo A": (1.5, 58, 0.2),
    "Pasillo B": (1.5, 56, 0.2),
    "Pasillo C": (1.5, 49, 0.2),
    "P.A1": (-5, 49, 0.2),
    "P.A2": (-5, 44, 0.2),
    "Pasillo D": (3,37, 0.2),
    "Pasillo E": (3, 33, 0.2),
    "Pasillo F": (3, 25, 0.2),
    "Pasillo G": (3, 17, 0.2),
    "Pasillo H": (3, 12, 0.2),
    "Pasillo I": (3, 2.5, 0.2),
    "Pasillo J": (3, -3, 0.2),
    "Pasillo K": (3, -0.5, 0.2),
    
    

    
    "Mediateca": (1.5, 65, 0.2),
    "Bedelía": (-7, 56, 0.2),
    "DOT": (-7, 44, 0.2),

   
    "Baño1": (0, 37, 0.2),
    "Baño2": (0, 33, 0.2),
    "Lab. Química": (0, 25, 0.2),
    "Lab. Biología": (0, 17, 0.2),
    "Salón 1": (0, -3, 0.2),
    "Salón 2": (0, -0.5, 0.2),
    "Salón 3": (0, 2.5, 0.2),
    "Salón 5": (0, 12, 0.2),
}

# ==========================================================
# POSICION INICIAL DEL GRAFO
# ==========================================================

START_NODE = "Entrada principal"

# ==========================================================
# CONEXIONES
# ==========================================================

EDGES = [

    ("Entrada principal", "Pasillo A"),
    ("Entrada principal", "Pasillo B"),
    ("Entrada principal", "Pasillo C"),
    ("Entrada principal", "P.A3"),
    ("P.A3", "Pasillo D"),
    ("P.A3", "Pasillo E"),
    ("P.A3", "Pasillo F"),
    ("P.A3", "Pasillo G"),
    ("P.A3", "Pasillo H"),
    ("P.A3", "Pasillo I"),
    ("P.A3", "Pasillo J"),
    ("P.A3", "Pasillo K"),
    
    
    ("Pasillo A", "Mediateca"),
    ("Pasillo B", "Bedelía"),
    ("Pasillo C", "P.A1"),
    ("P.A1", "P.A2"),
    ("P.A2", "DOT"),

    ("Pasillo D", "Baño1"),
    ("Pasillo E", "Baño2"),
    ("Pasillo F", "Lab. Química"),
    ("Pasillo G", "Lab. Biología"),

    ("Pasillo I", "Salón 3"),
    ("Pasillo K", "Salón 2"),
    ("Pasillo J", "Salón 1"),
    ("Pasillo H", "Salón 5"),
]

# ==========================================================
# APP PRINCIPAL
# ==========================================================

class CERPSWNavigator(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        # ==================================================
        # CONFIG VENTANA
        # ==================================================

        props = WindowProperties()
        props.setTitle("CERPSW Navigator 3D")

        self.win.requestProperties(props)

        self.setBackgroundColor(0.03, 0.03, 0.05)

        # ==================================================
        # DESACTIVAR CAMARA DEFAULT
        # ==================================================

        self.disableMouse()

        # ==================================================
        # CONTROL CAMARA
        # ==================================================

        self.heading = 45
        self.pitch = 90

        self.camera_distance = 125

        self.camera_target = Vec3(0,20, 0)

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        # ==================================================
        # LUCES
        # ==================================================

        self.setup_lights()

        # ==================================================
        # MODELO GLB
        # ==================================================

        self.map_model = self.loader.loadModel(
            "CeRPSW_con_nombre.glb"
        )

        self.map_model.reparentTo(self.render)

        # ==================================================
        # ORIENTACION CORRECTA
        # ==================================================

        # IMPORTANTE:
        # El modelo estaba vertical.
        # Esto lo rota correctamente.

        self.map_model.setHpr(180, 0, 0)

        # ESCALA
        self.map_model.setScale(1)

        # POSICION
        self.map_model.setPos(20, 20, 0)

        # ==================================================
        # GRAFO
        # ==================================================

        self.graph = nx.Graph()
        self.start_node = START_NODE

        for name, pos in LOCATIONS.items():

            self.graph.add_node(
                name,
                pos=pos
            )

        for a, b in EDGES:

            dist = self.distance(
                LOCATIONS[a],
                LOCATIONS[b]
            )

            self.graph.add_edge(
                a,
                b,
                weight=dist
            )

        # ==================================================
        # HUELLAS
        # ==================================================

        self.footsteps = []

        # ==================================================
        # UI
        # ==================================================

        self.setup_ui()

        # ==================================================
        # CAMARA INICIAL
        # ==================================================

        self.update_camera()

        # ==================================================
        # TASKS
        # ==================================================

        self.taskMgr.add(
            self.camera_task,
            "camera_task"
        )

    # ======================================================
    # LUCES
    # ======================================================

    def setup_lights(self):

        ambient = AmbientLight("ambient")

        ambient.setColor((0.8, 0.8, 0.85, 1))

        ambient_np = self.render.attachNewNode(ambient)

        self.render.setLight(ambient_np)

        directional = DirectionalLight("directional")

        directional.setColor((1, 1, 1, 1))

        directional_np = self.render.attachNewNode(
            directional
        )

        directional_np.setHpr(45, -45, 0)

        self.render.setLight(directional_np)

    # ======================================================
    # UI
    # ======================================================

    def setup_ui(self):

        self.panel = DirectFrame(
            frameColor=(0.07, 0.07, 0.1, 0.92),
            frameSize=(-0.42, 0.42, -1, 1),
            pos=(-1.28, 0, 0)
        )

        self.title = OnscreenText(
            text="CERPSW NAVIGATOR",
            pos=(-1.12, 0.9),
            scale=0.055,
            fg=(1, 1, 1, 1)
        )

        self.origin_text = OnscreenText(
            text=f"Origen: {self.start_node}",
            pos=(-1.1, 0.88),
            scale=0.035,
            fg=(0.8, 0.8, 1, 1)
        )

        self.destination_text = OnscreenText(
            text="Destino: Ninguno",
            pos=(-1.1, 0.82),
            scale=0.04,
            fg=(0.5, 0.9, 1, 1)
        )

        y = 0.68

        for location in LOCATIONS.keys():

            if "Pasillo" in location:
                continue
            if "P.A" in location:
                continue
            if location == "Entrada principal":
                continue

            DirectButton(
                text=location,
                scale=0.045,
                pos=(-1.1, 0, y),

                frameColor=(0.15, 0.35, 0.85, 1),

                text_fg=(1, 1, 1, 1),

                command=self.navigate_to,

                extraArgs=[location]
            )

            y -= 0.085

        # LIMPIAR

        DirectButton(
            text="Limpiar ruta",

            scale=0.045,

            pos=(-1.1, 0, -0.75),

            frameColor=(0.85, 0.2, 0.2, 1),

            text_fg=(1, 1, 1, 1),

            command=self.clear_path
        )

        # RESET CAMARA

        DirectButton(
            #text="Reset cámara",

            scale=0.0001,

            #pos=(-1.1, 0, -0.87),

            #frameColor=(0.2, 0.7, 0.3, 1),

            #
            #command=self.reset_camera
        )
    # ======================================================
    # NAVEGAR
    # ======================================================

    def navigate_to(self, destination):

        self.clear_path()

        self.destination_text.setText(
            f"Destino: {destination}"
        )

        path = nx.astar_path(
            self.graph,
            self.start_node,
            destination,
            heuristic=self.heuristic,
            weight="weight"
        )

        positions = []

        for node in path:

            pos = LOCATIONS[node]

            positions.append(
                Vec3(
                    pos[0],
                    pos[1],
                    pos[2] + 0.2
                )
            )

        self.animate_footsteps(positions)

    # ======================================================
    # HUELLAS
    # ======================================================

    def animate_footsteps(self, positions):

        sequence = Sequence()

        for i in range(len(positions) - 1):

            start = positions[i]
            end = positions[i + 1]

            steps = 15

            for s in range(steps):

                t = s / steps

                x = start.x + (end.x - start.x) * t
                y = start.y + (end.y - start.y) * t
                z = start.z + (end.z - start.z) * t

                pos = Vec3(x, y, z)

                sequence.append(
                    Func(
                        self.create_footstep,
                        pos
                    )
                )

                sequence.append(
                    Wait(0.02)
                )

        sequence.start()

    # ======================================================
    # HUELLA
    # ======================================================

    def create_footstep(self, pos):

        foot = self.loader.loadModel(
            "models/smiley"
        )

        foot.reparentTo(self.render)

        foot.setScale(0.09)

        foot.setPos(pos)

        foot.setColor(0, 1, 1, 1)

        foot.setTransparency(
            TransparencyAttrib.MAlpha
        )

        self.footsteps.append(foot)

    # ======================================================
    # LIMPIAR
    # ======================================================

    def clear_path(self):

        for foot in self.footsteps:
            foot.removeNode()

        self.footsteps.clear()

    # ======================================================
    # RESET CAMARA
    # ======================================================

    def reset_camera(self):

        self.heading = 0
        self.pitch = -35

        self.camera_distance = 65

        self.camera_target = Vec3(
            15,
            0,
            0
        )

        self.update_camera()

    # ======================================================
    # DISTANCIA
    # ======================================================

    def distance(self, a, b):

        return math.sqrt(
            (a[0] - b[0]) ** 2 +
            (a[1] - b[1]) ** 2 +
            (a[2] - b[2]) ** 2
        )

    # ======================================================
    # HEURISTICA
    # ======================================================

    def heuristic(self, a, b):

        return self.distance(
            LOCATIONS[a],
            LOCATIONS[b]
        )

    # ======================================================
    # ACTUALIZAR CAMARA
    # ======================================================

    def update_camera(self):

        heading_rad = math.radians(
            self.heading
        )

        pitch_rad = math.radians(
            self.pitch
        )

        x = (
            self.camera_target.x +
            self.camera_distance *
            math.cos(pitch_rad) *
            math.sin(heading_rad)
        )

        y = (
            self.camera_target.y -
            self.camera_distance *
            math.cos(pitch_rad) *
            math.cos(heading_rad)
        )

        z = (
            self.camera_target.z +
            self.camera_distance *
            math.sin(pitch_rad)
        )

        self.camera.setPos(x, y, z)

        self.camera.lookAt(
            self.camera_target
        )

    # ======================================================
    # CAMARA
    # ======================================================

    def camera_task(self, task):

        if self.mouseWatcherNode.hasMouse():

            mouse = self.mouseWatcherNode.getMouse()

            current_x = mouse.getX()
            current_y = mouse.getY()

            dx = current_x - self.last_mouse_x
            dy = current_y - self.last_mouse_y

            # ==========================================
            # ROTACION
            # CLICK DERECHO
            # ==========================================

            """if base.mouseWatcherNode.isButtonDown(
                "mouse3"
            ):

               self.heading -= dx * 120
               self.pitch += dy * 120

                self.pitch = max(
                    -89,
                    min(89, self.pitch)
                )

                self.update_camera()"""

            # ==========================================
            # MOVER CAMARA
            # CLICK CENTRAL
            # ==========================================
"""
            if base.mouseWatcherNode.isButtonDown(
                "mouse2"
            ):

                self.camera_target.x -= dx * 20
                self.camera_target.z += dy * 20

                self.update_camera()

            self.last_mouse_x = current_x
            self.last_mouse_y = current_y

        return Task.cont
"""
# ==========================================================
# ZOOM RUEDA MOUSE
# ==========================================================

app = CERPSWNavigator()
"""
# ZOOM
base.accept(
    "wheel_up",
    lambda: (
        setattr(
            app,
            "camera_distance",
            max(
                10,
                app.camera_distance - 3
            )
        ),
        app.update_camera()
    )
)

base.accept(
    "wheel_down",
    lambda: (
        setattr(
            app,
            "camera_distance",
            min(
                150,
                app.camera_distance + 3
            )
        ),
        app.update_camera()
    )
)
"""
# ==========================================================
# EJECUTAR
# ==========================================================

app.run()