import sys
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Contador(threading.Thread):
    def __init__(self, etiqueta):
        # Llamamos al "super" de la clase
        threading.Thread.__init__(self)

        # Establecemos variables necesarias
        self.evento = threading.Event()
        self.contador = 0
        self.etiqueta = etiqueta

        # Comenzamos el hilo
        self.start()

    def run(self):
        # Método sobrescrito (o sobreescrito, no sé cómo se escribe)
        # Mientras el evento no se cancele, refrescamos el valor de la etiqueta, aumentamos el contador
        # y esperamos un segundo. Esto sin afectar al proceso de la ventana, ya que corren en momentos
        # distintos
        while not self.evento.is_set():
            self.etiqueta.setText("Han transcurrido " + str(self.contador) + " segundo(s)")
            self.contador += 1
            self.evento.wait(1)

    def detener_contador(self):
        # No hacen falta comentarios
        self.evento.set()


class Aplicacion():
    def __init__(self):
        # Creamos una aplicación de PyQt
        self.app = QApplication(sys.argv)

        # Creamos una ventana y la ajustamos
        self.win = QWidget()

        # Caja contenedora

        self.vbox = QVBoxLayout()

        # Etiqueta para mostrar la información de los segundos transcurridos
        self.etiqueta_informacion = QLabel("Aquí se volcará la información", self.win)

        # Etiqueta para el nombre de usuario
        self.etiqueta_nombre_de_usuario = QLabel("Nombre de usuario:", self.win)

        # Etiqueta para contraseña:
        self.etiqueta_palabra_secreta = QLabel("Contraseña:", self.win)

        # Campo para el nombre de usuario
        self.input_nombre_de_usuario = QLineEdit("", self.win)

        # Campo para contraseña
        self.input_palabra_secreta = QLineEdit("", self.win)

        # Instanciamos un nuevo contador para que empiece a contar los segundos
        self.ayudante_contador = Contador(self.etiqueta_informacion)

        self.preparar_ventana()
        self.comenzar_contador()

    def comprueba_datos(self):
        # Definimos el usuario y contraseña correctos
        usuario_correcto = "foo"
        palabra_secreta_correcta = "bar"

        # Obtenemos lo que el usuario introdujo
        usuario_introducido = self.input_nombre_de_usuario.text()
        palabra_secreta_introducida = self.input_palabra_secreta.text()

        # Comprobamos si coinciden
        coinciden_los_datos = \
            usuario_introducido == usuario_correcto \
            and \
            palabra_secreta_introducida == palabra_secreta_correcta
        # En caso de que sí, detenemos el contador
        if coinciden_los_datos:
            self.detener_contador()

    def preparar_ventana(self):
        # Ponemos un tamaño fijo a la ventana. Así no se deforman los elementos
        self.win.setFixedSize(500, 150)

        # Preparar etiqueta para el contador
        self.etiqueta_informacion.setAlignment(Qt.AlignCenter)

        # Preparar caja de texto de usuario
        # Tamaño de la caja
        self.input_nombre_de_usuario.setMaximumSize(self.win.width(), 25)
        # Cuando el texto cambie, llamamos a comprueba_datos
        self.input_nombre_de_usuario.textChanged.connect(self.comprueba_datos)

        # Preparar caja de texto de contraseña.
        # Tamaño de la caja
        self.input_palabra_secreta.setMaximumSize(self.win.width(), 25)  # Ponemos tamaño
        # Cuando el texto cambie, llamamos a comprueba_datos
        self.input_palabra_secreta.textChanged.connect(self.comprueba_datos)
        # Le ponemos una máscara para que la contraseña no se vea
        self.input_palabra_secreta.setEchoMode(QLineEdit.Password)

        # Escuchamos cuando quieran detener a la app, así paramos el hilo y no se convierte en zombie
        self.app.aboutToQuit.connect(self.detener_contador)

        # Agregamos los componentes a la caja
        self.vbox.addWidget(self.etiqueta_informacion)
        self.vbox.addWidget(self.etiqueta_nombre_de_usuario)
        self.vbox.addWidget(self.input_nombre_de_usuario)
        self.vbox.addWidget(self.etiqueta_palabra_secreta)
        self.vbox.addWidget(self.input_palabra_secreta)

        # Establecemos una distribución para la app
        self.win.setLayout(self.vbox)

        # Ponemos un título
        self.win.setWindowTitle("Simular ejecución de procesos")

        # Mostramos la ventana
        self.win.show()

        # Salimos y ejecutamos la app
        sys.exit(self.app.exec_())

    def comenzar_contador(self):
        # Nos ayudamos de la clase Thread para empezar un hilo
        self.ayudante_contador.start()

    def detener_contador(self):
        # ¿Hace falta un comentario aquí?
        self.ayudante_contador.detener_contador()


if __name__ == '__main__':
    a = Aplicacion()
