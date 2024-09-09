class Protocols:

    class Response:
        #MENU = "protocol.menu"
        AUTH = "protocol.auth"
        PLAY = "protocol.play"
        CREDITS = "protocol.credits"
        QUIT = "protocol.quit"
        NICKNAME = "protocol.request_nickname"
        NICKNAME_ERROR = "protocol.request.nickname_error"
        REQUEST_GAME_ID = "protocol.request_game_id"
        WAITING_FOR_PAIR = "protocol.waiting_for_pair"
        LOBBY_CREATED = "protocol.lobby_created"
        JOINED_LOBBY = "protocol.joined_lobby"
        LOBBY_FULL = "protocol.lobby_full"
        LOBBY_NOT_FOUND = "protocol.lobby_not_found"
        GAME_STARTED = "protocol.game_started"
        START = "protocol.start"
        ANSWER_VALID = "protocol.answer_valid"
        ANSWER_INVALID = 'protocol.answer_invalid'
        PLAYER_LEFT = "protocol.player_left"
        REGISTER_REQUEST = "protocol.register_request"
        REGISTER_SUCCESS = "protocol.register_success"
        REGISTER_FAILED = "protocol.register_failed"
        DISCONNECTED_SUCCESS = "protocol.disconnected_success"
        DISCONNECTED_FAILED = "protocol.disconnected_failed"

    class Request:
        NICKNAME = "protocol.send_nickname"
        LEAVE = "protocol.leave"
        REGISTER = "protocol.register"