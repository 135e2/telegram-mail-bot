import logging
from imapclient import IMAPClient
from utils.mail import Email


logger = logging.getLogger(__name__)


class EmailClient(object):
    def __init__(self, email_account, passwd):
        self.email_account = email_account
        self.password = passwd
        self.server, self.number = self.connect(self)

    @staticmethod
    def connect(self):
        # parse the server's hostname from email account
        imap4_server = "mx1." + self.email_account.split("@")[-1]
        server = IMAPClient(host=imap4_server, use_uid=True)
        # display the welcome info received from server,
        # indicating the connection is set up properly
        logger.info(server.welcome)
        # authenticating
        server.login(self.email_account, self.password)
        return server, server.select_folder("INBOX")[b"EXISTS"]

    def get_mails_list(self):
        messages = self.server.search()
        dict = self.server.fetch(messages, "RFC822")
        return sorted(dict.items(), key=lambda e: e[0])  # Do resorts

    def get_mails_count(self):
        return self.number

    def get_mail_by_index(self, index):
        list = self.get_mails_list()
        msg_data = list[int(index)-1][1]
        return Email(msg_data[b"RFC822"])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            logger.info("exited normally\n")
            self.server.shutdown()
        else:
            logger.error("raise an exception! " + str(exc_type))
            self.server.logout()
            return False  # Propagate


if __name__ == "__main__":
    useraccount = "XXXXX"
    password = "XXXXXX"

    client = EmailClient(useraccount, password)
    num = client.get_mails_count()
    print(num)

    for uid, msg_data in client.get_mails_list().items():
        print(client.get_mail_by_index(uid))
