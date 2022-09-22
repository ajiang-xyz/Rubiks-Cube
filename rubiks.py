class Face:
    def __init__(self, text):
        # Given a flat string, break it into 3 arrays representing each row in the face.
        self.face = [
            [char for char in text[:3]],
            [char for char in text[3:6]],
            [char for char in text[6:]]
        ]

        # In any given rotation, the same "blocks" that were rotated out of a face must be replaced. Keep track of which blocks were moved
        #   out for easy replacement
        self.lastAccessed = []

    # Pretty print face in 3x3 grid
    def __str__(self):
        stringBuilder = []
        for row in self.face:
            stringBuilder.append("".join(row))
        return "\n".join(stringBuilder)

    def flattenToString(self):
        return "".join([value for row in self.face for value in row])

    # Given array of (x, y) coords, return an in-order array of the values in the face at those coords
    def getPositions(self, positionsArray):
        self.lastAccessed = []
        chars = []
        for pos in positionsArray:
            chars.append(self.face[pos[0]][pos[1]])
            self.lastAccessed.append(pos)
        return chars

    # Given a new set of values, replace the coords in the lastAccessed array in order
    def replacePositions(self, newCharsArray):
        for pos, char in zip(self.lastAccessed, newCharsArray):
            self.face[pos[0]][pos[1]] = char

    # Rotate entire face 90 degrees clockwise
    def rotate(self):
        temp = [
            self.getPositions([(2, 0), (1, 0), (0, 0)]),
            self.getPositions([(2, 1), (1, 1), (0, 1)]),
            self.getPositions([(2, 2), (1, 2), (0, 2)]),
        ]

        self.face = temp
        self.lastAccessed = []

class Cube:
    def __init__(self, text = False):
        if text:
            assert len(text) == 54
        else:
            # Standard cube net
            text = "wwwwwwwwwooogggrrrbbbooogggrrrbbbooogggrrrbbbyyyyyyyyy"

        # Given a flat string, break it into the correct faces
        self.cube = {
            "white" : Face(text[:9]),
            "orange" : Face(text[9:12] + text[21:24] + text[33:36]),
            "green" : Face(text[12:15] + text[24:27] + text[36:39]),
            "red" : Face(text[15:18] + text[27:30] + text[39:42]),
            "blue" : Face(text[18:21] + text[30:33] + text[42:45]),
            "yellow" : Face(text[45:]),
        }

        # Sets of 3 pieces on each face
        self.blocks = {
            "top" : [(0, 0), (0, 1), (0, 2)],
            "left" : [(2, 0), (1, 0), (0, 0)],
            "right" : [(0, 2), (1, 2), (2, 2)],
            "bottom" : [(2, 2), (2, 1), (2, 0)]
        }

    # Pretty print cube in standard net form
    def __str__(self):
        stringBuilder = """
    {0}{1}{2}
    {3}{4}{5}
    {6}{7}{8}
{9}{10}{11} {18}{19}{20} {27}{28}{29} {36}{37}{38}
{12}{13}{14} {21}{22}{23} {30}{31}{32} {39}{40}{41}    
{15}{16}{17} {24}{25}{26} {33}{34}{35} {42}{43}{44}    
    {45}{46}{47}
    {48}{49}{50}
    {51}{52}{53}
"""
        flattenedValues = ""
        for face in self.cube.values():
            flattenedValues += face.flattenToString()
        return stringBuilder.format(*list(flattenedValues))

    def flatten(self):
        stringBuilder = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{18}{19}{20}{27}{28}{29}{36}{37}{38}{12}{13}{14}{21}{22}{23}{30}{31}{32}{39}{40}{41}{15}{16}{17}{24}{25}{26}{33}{34}{35}{42}{43}{44}{45}{46}{47}{48}{49}{50}{51}{52}{53}"
        flattenedValues = ""
        for face in self.cube.values():
            flattenedValues += face.flattenToString()
        return stringBuilder.format(*list(flattenedValues))

    # Parse an algorithm string and execute Cube methods
    def solve(self, alg):
        for rotation in alg.split():
            parsedAlg = []
            if "'" in rotation:
                parsedAlg.append(getattr(self, rotation[0]))
                parsedAlg.append(getattr(self, rotation[0]))
                parsedAlg.append(getattr(self, rotation[0]))
            elif "2" in rotation:
                parsedAlg.append(getattr(self, rotation[0]))
                parsedAlg.append(getattr(self, rotation[0]))
            else:
                parsedAlg.append(getattr(self, rotation[0]))
            for move in parsedAlg:
                move()

    # Common function for all FRUBLD face rotations
    def turn(self, setCycle, rotationFace, blockMap):
        values = []
        for color, position in blockMap.items():
            values.append(self.cube[color].getPositions(self.blocks[position]))
        for color, value in zip(setCycle, values):
            self.cube[color].replacePositions(value)
        self.cube[rotationFace].rotate()

    # Values specific for each rotation
    def F(self):
        setCycle = ["red", "white", "yellow", "orange"]
        rotationFace = "green"
        blockMap = {
            "white" : "bottom",
            "orange" : "right",
            "red" : "left",
            "yellow" : "top"
        }

        self.turn(setCycle, rotationFace, blockMap)

    def R(self):
        setCycle = ["blue", "white", "yellow", "green"]
        rotationFace = "red"
        blockMap = {
            "white" : "right",
            "green" : "right",
            "blue" : "left",
            "yellow" : "right"
        }

        self.turn(setCycle, rotationFace, blockMap)

    def U(self):
        setCycle = ["blue", "orange", "green", "red"]
        rotationFace = "white"
        blockMap = {
            "orange" : "top",
            "green" : "top",
            "red" : "top",
            "blue" : "top"
        }
        
        self.turn(setCycle, rotationFace, blockMap)

    def B(self):
        setCycle = ["orange", "yellow", "white", "red"]
        rotationFace = "blue"
        blockMap = {
            "white" : "top",
            "orange" : "left",
            "red" : "right",
            "yellow" : "bottom"
        }
        
        self.turn(setCycle, rotationFace, blockMap)

    def L(self):
        setCycle = ["green", "yellow", "white", "blue"]
        rotationFace = "orange"
        blockMap = {
            "white" : "left",
            "green" : "left",
            "blue" : "right",
            "yellow" : "left"
        }
        
        self.turn(setCycle, rotationFace, blockMap)

    def D(self):
        setCycle = ["green", "red", "blue", "orange"]
        rotationFace = "yellow"
        blockMap = {
            "orange" : "bottom",
            "green" : "bottom",
            "red" : "bottom",
            "blue" : "bottom"
        }
        
        self.turn(setCycle, rotationFace, blockMap)

# Invert an algorithm. Doing the original algorithm and the inverted algorithm yields the original state of the cube
def revAlg(alg):
    newAlg = []
    for rotation in alg.split():
        if "'" in rotation:
            newAlg.append(rotation[0])
        elif "2" not in rotation:
            newAlg.append(rotation[0] + "'")
        else:
            newAlg.append(rotation)
    return " ".join(newAlg[::-1])


# Flag :)
cube = Cube("_mwl{h}i_innihyosu_sOvtm_snsuo__Llgtfhepgtetoacay_Li__")
givenAlgorithm = "B2 R2 L' F' U D2 D' L' U2 F2 B U R' L' L F' U' U U' F U2 R' D F D2 B F' L' B2 L D2 L R2 L2 L2 R U2 D2 B' D' L2 R B2 U L U2 L F' R L"
solveAlgorithm = revAlg(givenAlgorithm)

print("Unsolved cube:")
print(cube)

print(f"Given algorithm: {givenAlgorithm}")
print(f"Solve algorithm: {solveAlgorithm}")

print("Solved cube:")
cube.solve(solveAlgorithm)
print(cube)

print(f"Flag: {cube.flatten()}")
