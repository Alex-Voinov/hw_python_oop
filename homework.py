from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE: ClassVar[str] = (
        'Тип тренировки: {training_type};'
        ' Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км;'
        ' Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MINS_IN_HOURS: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[int] = 18
    COEFF_CALORIE_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIE_1
             * self.get_mean_speed() - self.COEFF_CALORIE_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.MINS_IN_HOURS
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float
    COEFF_CALORIE_1: ClassVar[float] = 0.035
    COEFF_CALORIE_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIE_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.COEFF_CALORIE_2 * self.weight)
            * self.duration * self.MINS_IN_HOURS
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_1: ClassVar[float] = 1.1
    COEFF_CALORIE_2: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2 * self.weight
        )


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    CODES_AND_CLASSES: Dict[str, Type(Training)] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in CODES_AND_CLASSES:
        raise ValueError()
    else:
        return CODES_AND_CLASSES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
