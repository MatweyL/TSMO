import numpy as np
from matplotlib import pyplot as plt

HAIRCUT_COST = 60
CLEAN_INCOMING_COEFFICIENT = 0.3
BARBER_WORK_HOURS = 6
BARBERS_COUNT = 2

def calculate(client_period: float, haircut_average_time: float) -> float:
    client_flow_intensity = 60 / client_period
    service_flow_intensity = 60 / haircut_average_time

    barber_load_intensity = client_flow_intensity / service_flow_intensity
    # barber_downtime_probability = 1 - barber_load_intensity
    #
    # if ( 1 - barber_downtime_probability) != 0:
    #     average_clients_in_queue = barber_load_intensity ** 2 / (1 - barber_load_intensity)
    #     average_waiting_time_in_queue = average_clients_in_queue / client_flow_intensity
    #     average_clients_time_in_barbershop = average_waiting_time_in_queue + haircut_average_time
    barber_work_time = barber_load_intensity * BARBER_WORK_HOURS * 60
    clients_per_work_time = barber_work_time / haircut_average_time

    incoming = clients_per_work_time * HAIRCUT_COST
    clean_incoming = incoming * CLEAN_INCOMING_COEFFICIENT
    total_barbers_clean_incoming = clean_incoming * BARBERS_COUNT
    return total_barbers_clean_incoming


def main():
    # Создаем данные
    points_number = 64
    l_step = (25 - 15) / points_number
    client_period_range = [15 + i * l_step for i in range(points_number)]

    m_step = (30 - 20) / points_number
    haircut_average_time_range = [20 + i * m_step for i in range(points_number)]
    client_period_range, haircut_average_time_range = np.meshgrid(client_period_range, haircut_average_time_range)

    function_values = np.array([calculate(client_period, haircut_average_time)
                                for client_period, haircut_average_time in
                                zip(client_period_range.flatten(), haircut_average_time_range.flatten())])
    function_values = function_values.reshape(client_period_range.shape)

    # Создаем фигуру и оси
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Строим поверхность
    ax.plot_surface(client_period_range, haircut_average_time_range, function_values, cmap='viridis')

    # Добавляем метки осей
    ax.set_xlabel('Период появления клиентов')
    ax.set_ylabel('Среднее время стрижки')
    ax.set_zlabel('Общий доход парикмахерской')

    # Показываем график
    plt.show()


if __name__ == '__main__':
    main()
