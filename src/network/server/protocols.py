class Protocols:

    class Response:
        NICKNAME = "protocol.request_nickname"
        NICKNAME_ERROR = "protocol.request.nickname_error"
        WAITING_FOR_PAIR = "protocol.waiting_for_pair"
        LOBBY_CREATED = "protocol.lobby_created"
        JOINED_LOBBY = "protocol.joined_lobby"
        LOBBY_FULL = "protocol.lobby_full"
        START = "protocol.start"
        ANSWER_VALID = "protocol.answer_valid"
        ANSWER_INVALID = 'protocol.answer_invalid'
        WINNER = "protocol.winner"
        PLAYER_LEFT = "protocol.opponent_left"

    class Request:
        NICKNAME = "protocol.send_nickname"
        LEAVE = "protocol.leave"