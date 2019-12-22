import random

NAMES = (
    'Ana', 'Alicia', 'Amalia', 'Adela', 'Alba', 'Alejandro', 'Alberto', 'Alfonso', 'Aaron', 'Alfredo',
    'Beatriz', 'Blanca', 'Begoña', 'Belén', 'Bienvenida', 'Braulio', 'Bernardo', 'Blas', 'Bartolomé', 'Bertín',
    'Carmen', 'Cecilia', 'Concha', 'Claudia', 'Cristina', 'Cristóbal', 'César', 'Carlos', 'Cayetano', 'Constantino',
    'Diana', 'Débora', 'Dolores', 'Dora', 'Dámaris', 'Darío', 'Daniel', 'David', 'Diego', 'Damián',
    'Elena', 'Ester', 'Elisa', 'Eva', 'Elvira', 'Ernesto', 'Ezequiel', 'Eugenio', 'Eulogio', 'Elián',
    'Francisca', 'Felisa', 'Florentina', 'Fátima', 'Florinda', 'Felipe', 'Francisco', 'Fernando', 'Feliciano', 'Félix',
    'Gemma', 'Gisella', 'Genoveva', 'Ginebra', 'Gilda', 'Gabriel', 'Gonzalo', 'Gregorio', 'Ginés', 'Guzmán',
    'Helena', 'Heidi', 'Herminia', 'Helga', 'Hilaria', 'Hipólito', 'Higinio', 'Hernán', 'Humberto', 'Hermes',
    'Inmaculada', 'Isabel', 'Irene', 'Itziar', 'Inés', 'Ildefonso', 'Iván', 'Ismael', 'Iñaki', 'Ignacio',
    'Julia', 'Jennifer', 'Jacinta', 'Jessica', 'Judith', 'José', 'Juan', 'Jorge', 'Jesús', 'Julián',
    'Laura', 'Lucía', 'Lola', 'Leonor', 'Lidia', 'Lucas', 'Lorenzo', 'Leopoldo', 'Leandro', 'Lázaro',
    'María', 'Mara', 'Marta', 'Marina', 'Mercedes', 'Miguel', 'Manuel', 'Mariano', 'Marcos', 'Marcelo',
    'Nuria', 'Natalia', 'Nerea', 'Nieves', 'Noelia', 'Nuño', 'Narciso', 'Néstor', 'Nicolás', 'Noé',
    'Olvido', 'Ofelia', 'Olivia', 'Olga', 'Olimpia', 'Octavio', 'Olegario', 'Oriol', 'Oscar', 'Omar',
    'Paula', 'Penélope', 'Pilar', 'Paloma', 'Patricia', 'Pablo', 'Pedro', 'Pascual', 'Pelayo', 'Pepe',
    'Raquel', 'Rocío', 'Ruth', 'Rebeca', 'Rosa', 'Roberto', 'Rodrigo', 'Ricardo', 'Ramón', 'Rubén',
    'Sofía', 'Susana', 'Sara', 'Soledad', 'Silvia', 'Sergio', 'Salvador', 'Sancho', 'Sebastián', 'Samuel',
    'Trinidad', 'Teresa', 'Tamara', 'Tina', 'Tecla', 'Teodoro', 'Tomás', 'Tristán', 'Tadeo', 'Tobías',
    'Úrsula', 'Uxue', 'Unax', 'Unai','Verónica', 'Virginia', 'Violeta', 'Victoria', 'Víctor', 'Vicente', 'Valentín',
)

SURNAMES = (
    'Sánchez', 'Fernández', 'González', 'López', 'García', 'Pérez', 'Martínez', 'Montesinos', 'Navarro', 'Jiménez',
    'Vélez', 'Ruiz', 'Peñalver', 'Soto', 'Valero', 'Pallarés', 'Nadal', 'Moya', 'Hernández', 'Ros', 'Castejón',
    'Noguera', 'Otero', 'Herrera', 'Alsina', 'Bueno', 'Reyes', 'Barceló', 'Aguirre', 'Cortés', 'Pizarro', 'Dols',
    'Manrique', 'Alburquerque', 'Asencio', 'Arnaldos', 'Cegarra', 'Meroño', 'Mercader', 'Maturana', 'Villada',
    'Melero', 'Saura', 'Ferrándiz', 'Anguita', 'Garzón', 'Rajoy', 'Iglesias', 'Rivera', 'Casado', 'Zapatero',
    'Rivas', 'Monegal', 'Bretos', 'Blanco', 'Briones', 'Cayuela', 'Boyero', 'Hidalgo', 'Torres', 'Valenzuela',
    'Blaya', 'Salas', 'Alcaraz', 'Albaladejo', 'Lorca', 'Goya', 'Velázquez', 'Vázquez', 'Segura', 'Fuentes',
    'Puyol', 'Aznar', 'Montero', 'Suárez', 'Altozano', 'Otón', 'Alarcón', 'Cabañero', 'Pedreño', 'Díaz', 'Díez',
    'Lajarín', 'Mora', 'Morales', 'Medrano', 'Cruz', 'Castro', 'Rodríguez', 'Ortín', 'Velasco', 'Méndez', 'Casal',
    'Muñoz', 'Silvestra', 'Alborán', 'Casas', 'Ortiz', 'Rico', 'Herrán', 'Lorente', 'Tortosa', 'Merlo', 'Pujades',
    'Albarracín', 'Gutiérrez', 'Tejón', 'Guirao', 'Montes', 'Sevilla', 'Gómez', 'Expósito', 'Cebrián', 'Calleja',
    'Canales', 'Cardeñosa', 'Casasola', 'Rueda', 'Adánez', 'Lastra', 'Calvo', 'Poveda', 'Alonso', 'Cuevas'
)


def get_random_name():
    """
    Generates a random name from the above name and surname pools.
    :return: a randomly generated name.
    :rtype: str
    """
    fullname = f'{random.choice(NAMES)} {random.choice(SURNAMES)}'
    return fullname
