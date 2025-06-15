import threading


class SemanticErrorHandler:
    def __init__(self, print_enable=True, max_errors=1000):
        self.errors = []
        self.print_enable = print_enable
        self.max_errors = max_errors
        self._lock = threading.Lock()

    def report(self, message, lineno=None):
        try:
            if not isinstance(message, str):
                message = str(message)
            if lineno is not None and not isinstance(lineno, int):
                lineno = str(lineno)
            if lineno:
                msg = f"[语义错误] 第{lineno}行: {message}"
            else:
                msg = f"[语义错误] {message}"
            with self._lock:
                if len(self.errors) < self.max_errors:
                    self.errors.append(msg)
            if self.print_enable:
                print(msg)
        except Exception as e:
            print(f"[SemanticErrorHandler内部异常] {e}")

    def has_errors(self):
        return len(self.errors) > 0

    def get_all(self):
        return self.errors.copy()
    
    def get_errors(self):
        """获取所有错误信息"""
        return self.errors.copy()
