class Protocols:

    class Response:
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
        WINNER = "protocol.winner"
        PLAYER_LEFT = "protocol.opponent_left"
        REGISTER_REQUEST = "REGISTER_REQUEST"
        REGISTER_SUCCESS = "REGISTER_SUCCESS"
        REGISTER_FAILED = "REGISTER_FAILED"
        DISCONNECTED_SUCCESS = "DISCONNECTED_SUCCESS"
        DISCONNECTED_FAILED = "DISCONNECTED_FAILED"

    class Request:
        NICKNAME = "protocol.send_nickname"
        LEAVE = "protocol.leave"
        REGISTER = "REGISTER"