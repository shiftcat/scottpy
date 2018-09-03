

class ContentsNotFoundException(Exception):
    """
    이 클래스는 조회결과가 존재하지 않을 경우 발생할 예외 클래스이다.

    - 속성 -
        message: 예외에 대한 메시지
        status: 상태코드
    """

    def __init__(self, message, status=404):
        self.message = message
        self.status = status


    def __str__(self):
        return self.message


    def get_message(self):
        """
        예외에 대한 메시지를 리턴한다.
        :return: 예외 메시지
        """
        return self.message


    def get_status(self):
        """
        예외에 대한 상태 코드를 리턴한다.
        :return: 예외 상태 코드
        """
        return self.status