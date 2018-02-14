from db_menedger import connect_mysql
import app, time

not_connection_with_the_vodomat       = 'Нет связи с водоматом'
you_have_succeed_connected_to_vodomat = 'Вы успешно подключились к %s водомату'
you_have_already_connected_to_other   = 'Вы уже подключены к другому водомату, перед подключением вам сначала следует закрыть соединение с другим водоматом'
the_vodomat_is_busy                   = '%s водомат занят другим пользователем'
not_such_vodomat                      = 'Вы ввели id несуществующего водомата или этот водомат еще не был добавлен, на сервер'


# Проверка состояния водомата
def check_stauts_of_vodomat(wm):
    StatusOfVodomat = connect_mysql.select_status_of_vodomat(wm)
    response = {}

    if StatusOfVodomat != {}:
        if StatusOfVodomat['state'] == 'WAIT' or StatusOfVodomat['state'] == 'WORK' or StatusOfVodomat['state'] == 'JUST_PAID' or StatusOfVodomat['state'] == 'NO_WATER':
            Settings_of_vodomat = connect_mysql.select_action_of_vodomat(wm)
            if Settings_of_vodomat['action'] == '0':

                try:
                    last_save = app.last_save[wm].get('last_save')
                except:
                    response = not_connection_with_the_vodomat

                if last_save > (time.time() - 10):
                    response = True
        else:
            response = the_vodomat_is_busy

    else:
        response = not_such_vodomat

    return response


# Проверка состояния пользователя
def check_status_of_user(telegram):
    responce = 0

    cheking_user = connect_mysql.select_user(telegram)

    if cheking_user['wm'] != 0:

        if connect_mysql.select('wm_properties', 'wm = %s' % cheking_user['wm'], *['action'])['action'] == '1':

            responce = 1
            print(
                'Пользователь занят')
        else:
            print(
                'Пользователь свободен, но ранее в ходе отключения не был обнулен параметр, который отвечает какой водомат занял пользователь')
    else:
        print('Пользователь свободен')

    return responce

def score_of_user(telegram):
    return connect_mysql.select_scoreof_user(telegram)