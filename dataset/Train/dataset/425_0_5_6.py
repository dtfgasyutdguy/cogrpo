# Code in 2.7 needing rule:
#   try_except ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK except_handler
# Generally we need a COME_FROM. But not in the situation below.


    try:
# for package in [1,2]:
        pass
    except IndexError:
        with __file__ as f:
            pass
    except:
        raise
