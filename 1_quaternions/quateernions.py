import numpy as np

class Quaternion:
    """
    Класс для представления кватерниона.
    """

    def __init__(self, w=0.0, x=0.0, y=0.0, z=0.0):
        """
        Инициализирует кватернион.
        """
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """
        Возвращает строковое представление кватерниона.
        """
        return f"({self.w}, {self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        """
        Сложение кватернионов.
        """
        return Quaternion(self.w + other.w,
                          self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    def __sub__(self, other):
        """
        Вычитание кватернионов.
        """
        return Quaternion(self.w - other.w,
                          self.x - other.x,
                          self.y - other.y,
                          self.z - other.z)

    def __mul__(self, other):
        """
        Умножение кватернионов.
        """
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        else:
            return Quaternion(self.w * other,
                              self.x * other,
                              self.y * other,
                              self.z * other)

    def conjugate(self):
        """
        Возвращает сопряженный кватернион.
        """
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm(self):
        """
        Возвращает норму кватерниона.
        """
        return np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def inverse(self):
        """
        Возвращает обратный кватернион.
        """
        norm_sq = self.norm() ** 2
        if norm_sq == 0:
            raise ValueError("Норма кватерниона равна нулю. Невозможно вычислить обратный кватернион.")
        return Quaternion(self.w * (1 / norm_sq),
                          -self.x * (1 / norm_sq),
                          -self.y * (1 / norm_sq),
                          -self.z * (1 / norm_sq))

    @staticmethod
    def from_axis_angle(axis, angle):
        """
        Создает кватернион вращения из оси и угла.
        """
        axis = axis / np.linalg.norm(axis)  # Нормализация оси
        half_angle = angle / 2.0
        w = np.cos(half_angle)
        x = np.sin(half_angle) * axis[0]
        y = np.sin(half_angle) * axis[1]
        z = np.sin(half_angle) * axis[2]
        return Quaternion(w, x, y, z)

    def rotate(self, vector):
        """
        Поворачивает вектор с помощью кватерниона вращения.
        """
        q_conj = self.conjugate()
        q_vec = Quaternion(0.0, vector[0], vector[1], vector[2])
        rotated_q = self * q_vec * q_conj
        return np.array([rotated_q.x, rotated_q.y, rotated_q.z])

if __name__ == '__main__':
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(5, 6, 7, 8)

    print("q1:", q1)
    print("q2:", q2)

    print("q1 + q2:", q1 + q2)
    print("q1 - q2:", q1 - q2)
    print("q1 * q2:", q1 * q2)

    # Вращение вектора
    axis = np.array([1, 0, 0])  # Ось вращения (x)
    angle = np.pi / 2  # Угол вращения (90 градусов)
    rotation_q = Quaternion.from_axis_angle(axis, angle)

    vector = np.array([0, 1, 0])  # Вектор, который нужно повернуть
    rotated_vector = rotation_q.rotate(vector)

    print(f"Вектор {vector} после вращения: {rotated_vector}")
