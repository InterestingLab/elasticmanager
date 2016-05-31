class IndexSetError(Exception):
    pass


class CanNotAliasIndex(IndexSetError):
    pass


class CanNotCreateIndex(IndexSetError):
    pass


class CanNotCloseIndex(IndexSetError):
    pass


class CanNotDeleteIndex(IndexSetError):
    pass


class CanNotOptimizeIndex(IndexSetError):
    pass


class CanNotSnapshotIndex(IndexSetError):
    pass

class CanNotReplicateIndex(IndexSetError):
    pass

class CanNotRelocateIndex(IndexSetError):
    pass
