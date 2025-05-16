from abc import ABC, abstractmethod

class Vehiculo(ABC):
    def __init__(self, marca, modelo, año, placa, costo_diario):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.placa = placa
        self.costo_diario = costo_diario
        self.alquilado = False

    @abstractmethod
    def calcular_costo_alquiler(self, dias, kilometros):
        pass

    @abstractmethod
    def requisitos_alquiler(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.marca} {self.modelo} ({self.año}), Placa: {self.placa}"

    def _calcular_costo(self, dias, km, max_km, tarifa_extra, recargo=0):
        base = self.costo_diario * dias
        km_permitidos = max_km * dias
        km_extra = max(0, km - km_permitidos)
        extra = km_extra * tarifa_extra + recargo
        return {
            'costo_base': base,
            'costo_extra': extra,
            'total': base + extra,
            'dias': dias,
            'km_extra': km_extra
        }

# === CARRO ===
class Carro(Vehiculo):
    KM_MAX = 200
    TARIFA_EXTRA = 0.5

    def calcular_costo_alquiler(self, dias, kilometros):
        return self._calcular_costo(dias, kilometros, self.KM_MAX, self.TARIFA_EXTRA)

    def requisitos_alquiler(self):
        return "Requisitos para alquilar carro:\n- Licencia tipo B\n- Documento de identidad\n- Tarjeta de crédito"

# === MOTO ===
class Moto(Vehiculo):
    KM_MAX = 150
    TARIFA_EXTRA = 0.3
    RECARGO_CILINDRADA = 0.1
    CILINDRADA_LIMITE = 500

    def __init__(self, marca, modelo, año, placa, costo_diario, cilindrada):
        super().__init__(marca, modelo, año, placa, costo_diario)
        self.cilindrada = cilindrada

    def calcular_costo_alquiler(self, dias, kilometros):
        recargo = 0
        if self.cilindrada > self.CILINDRADA_LIMITE:
            recargo = self.costo_diario * dias * self.RECARGO_CILINDRADA
        return self._calcular_costo(dias, kilometros, self.KM_MAX, self.TARIFA_EXTRA, recargo)

    def requisitos_alquiler(self):
        return "Requisitos para alquilar moto:\n- Licencia tipo A\n- Documento de identidad\n- Casco propio o pago adicional"

# === CAMIONETA ===
class Camioneta(Vehiculo):
    KM_MAX = 180
    TARIFA_EXTRA = 0.7
    RECARGO_CAPACIDAD = 0.15
    LIMITE_CAPACIDAD = 1000

    def __init__(self, marca, modelo, año, placa, costo_diario, capacidad_carga):
        super().__init__(marca, modelo, año, placa, costo_diario)
        self.capacidad_carga = capacidad_carga

    def calcular_costo_alquiler(self, dias, kilometros):
        recargo = 0
        if self.capacidad_carga > self.LIMITE_CAPACIDAD:
            recargo = self.costo_diario * dias * self.RECARGO_CAPACIDAD
        return self._calcular_costo(dias, kilometros, self.KM_MAX, self.TARIFA_EXTRA, recargo)

    def requisitos_alquiler(self):
        return "Requisitos para alquilar camioneta:\n- Licencia tipo C\n- Documento de identidad\n- Tarjeta de crédito\n- Verificación de historial de manejo"

# === ALQUILER ===
class Alquiler:
    def __init__(self, vehiculo, cliente, dias, kilometros_estimados):
        self.vehiculo = vehiculo
        self.cliente = cliente
        self.dias = dias
        self.kilometros_estimados = kilometros_estimados
        self.detalle_costo = vehiculo.calcular_costo_alquiler(dias, kilometros_estimados)
        vehiculo.alquilado = True

    def __str__(self):
        return (
            f"Alquiler de {self.vehiculo}\n"
            f"Cliente: {self.cliente}\n"
            f"Días de alquiler: {self.dias} (${self.vehiculo.costo_diario}/día)\n"
            f"Costo por días: ${self.detalle_costo['costo_base']:.2f}\n"
            f"Kilómetros extra: {self.detalle_costo['km_extra']} km\n"
            f"Costo por extras: ${self.detalle_costo['costo_extra']:.2f}\n"
            f"TOTAL: ${self.detalle_costo['total']:.2f}"
        )

# === SISTEMA DE ALQUILER ===
class SistemaAlquiler:
    def __init__(self):
        self.vehiculos = []
        self.alquileres = []

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def alquilar_vehiculo(self, placa, cliente, dias, kilometros):
        for vehiculo in self.vehiculos:
            if vehiculo.placa == placa and not vehiculo.alquilado:
                self.alquileres.append(Alquiler(vehiculo, cliente, dias, kilometros))
                return True
        return False

    def generar_reporte_alquileres(self):
        print("\n=== REPORTE DE ALQUILERES ===")
        for i, alquiler in enumerate(self.alquileres, 1):
            print(f"\nAlquiler #{i}:\n{alquiler}\n----------------------------")
        
        total = sum(alq.detalle_costo['total'] for alq in self.alquileres)
        print(f"\nTotal recaudado: ${total:.2f}")
        print(f"Vehículos alquilados actualmente: {len(self.alquileres)}/{len(self.vehiculos)}")

sistema = SistemaAlquiler()

# Agregar vehículos al sistema
sistema.agregar_vehiculo(Carro("Toyota", "Corolla", 2022, "ABC123", 50.0))
sistema.agregar_vehiculo(Moto("Honda", "CBR600", 2021, "XYZ789", 30.0, 600))
sistema.agregar_vehiculo(Camioneta("Ford", "Ranger", 2023, "DEF456", 70.0, 1200))

# Realizar alquileres
sistema.alquilar_vehiculo("ABC123", "Juan Pérez", 5, 1200)
sistema.alquilar_vehiculo("XYZ789", "María Gómez", 3, 600)

# Generar reporte
sistema.generar_reporte_alquileres()

# Mostrar requisitos de cada vehículo
for vehiculo in sistema.vehiculos:
    print("\n" + vehiculo.requisitos_alquiler())