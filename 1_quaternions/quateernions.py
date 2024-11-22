import math

class Quaternion:
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.w:.2f} + {self.x:.2f}i + {self.y:.2f}j + {self.z:.2f}k"

    def __add__(self, other):
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Quaternion): # Умножение кватерниона на кватернион
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        else: # Умножение кватерниона на скаляр
            return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other): # Для умножения скаляра на кватернион
        return self * other

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm(self):
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        n = self.norm()
        if n == 0:
            return self  # Avoid division by zero
        return Quaternion(self.w / n, self.x / n, self.y / n, self.z / n)

    def inverse(self):
        n = self.norm()
        if n == 0:
            return None # Обратный кватернион не существует для нулевого кватерниона
        return self.conjugate() / (n**2)


# Примеры использования:

q1 = Quaternion(1, 2, 3, 4)
q2 = Quaternion(5, 6, 7, 8)

print(f"q1: {q1}")
print(f"q2: {q2}")

q3 = q1 + q2
print(f"q1 + q2: {q3}")

q4 = q1 - q2
print(f"q1 - q2: {q4}")

q5 = q1 * q2
print(f"q1 * q2: {q5}")

q6 = 2 * q1 # Скалярное умножение
print(f"2 * q1: {q6}")

q7 = q1.conjugate()
print(f"Conjugate of q1: {q7}")

norm_q1 = q1.norm()
print(f"Norm of q1: {norm_q1}")

q8 = q1.normalize()
print(f"Normalized q1: {q8}")

q9 = q1.inverse()
print(f"Inverse of q1: {q9}")