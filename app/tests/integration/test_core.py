from typing import Iterator
import pytest


class TestPositiveCore:
    
    def testMainLoop(self, app) -> None:
        inputs: Iterator = iter(['exit'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)
        assert app.is_running == False

    def testMainLoop2(self, app) -> None:
        inputs: Iterator = iter(['q'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)
        assert app.is_running == False

    @pytest.mark.regression
    def testLogin(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', 'hello there', 'exit'])        

        app.start_app(input_method=lambda _: next(inputs), debug=True)
        
        out: str = capsys.readouterr().out.strip()
        assert 'Unknown option' in out

    @pytest.mark.regression
    def testRegister(self, app, capsys) -> None:
        inputs: Iterator = iter(['2', 'Newname', 'Strongpass!', 'Strongpass!', 'exit'])
        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'Password deos not match' not in out

    @pytest.mark.regression
    def testAfterLogin(self, app) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', 'q', 'exit'])
        app.start_app(input_method=lambda _: next(inputs), debug=True)
        assert app.is_running == False

    def testAfterLogin2(self, app) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', 'exit'])
        app.start_app(input_method=lambda _: next(inputs), debug=True)
        assert app.is_running == False

    @pytest.mark.regression
    def testAfterLoginCheckTaxes(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', '1', 'exit'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'water' in out


    def testAfterLoginPayTaxesHelp(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', '2', 'help', 'exit'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'water' in out

    def testAfterLoginPayTaxesNoHelp(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', '2', 'exit'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'water' not in out

    @pytest.mark.regression
    def testAfterLoginPayTaxesPayWater(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', '2', 'help', 'water',
                                 'y', '100', 'exit'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'water' in out
        assert 'water paid successfully' in out

    @pytest.mark.regression
    def testAfterLoginPayTaxesPayWaterCancel(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', 'test', '2', 'help', 'water',
                                 'n', 'exit'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'water' in out
        assert 'water paid successfully' not in out
        assert 'Aborted' in out


class TestNegativeCore:

    def testMainLoop(self, app, capsys) -> None:
        inputs: Iterator = iter(['eh?', 'q'])

        app.start_app(input_method=lambda _: next(inputs), debug=True)
        assert app.is_running == False
        out: str = capsys.readouterr().out.strip()
        assert 'Unknown option' in out

    def testMainLoopNoRun(self, app, capsys) -> None:
        assert app.is_running == False
        app.main_loop(input_method=lambda _: next(iter(['whom'])))
        out: str = capsys.readouterr().out.strip()
        assert 'Unknown option' not in out

    def testDoubleStart(self, app) -> None:
        app.is_running = True
        assert app.is_running == True

        with pytest.raises(RuntimeError, match='App is already running'):
            app.start_app()

    @pytest.mark.regression
    def testLoginEmptyPassword(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', '', 'hello there', 'exit'])        

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'cannot be empty' in out
        
    @pytest.mark.regression
    def testLoginEmptyName(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', '', 'test', 'hello there', 'exit'])        

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'cannot be empty' in out

    @pytest.mark.regression
    def testLoginWrongPassword(self, app, capsys) -> None:
        inputs: Iterator = iter(['1', 'test', 'wrong', 'hello there', 'exit'])        

        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'Incorrect' in out

    @pytest.mark.regression
    def testRegisterPasswordMismatch(self, app, capsys) -> None:
        inputs: Iterator = iter(
            [
                '2', 'Newname', 'Strongpass!', 'Strongpass?', 
                'Strongpass!', 'Strongpass!', 'exit'
            ]
        )
        app.start_app(input_method=lambda _: next(inputs), debug=True)

        out: str = capsys.readouterr().out.strip()
        assert 'Password does not match' in out

    @pytest.mark.regression
    def testRegisterEmptyName(self, app) -> None:
        inputs: Iterator = iter(['2', '', 'Strongpass!', 'Strongpass!', 'exit'])

        with pytest.raises(ValueError, match='Username cannot contain special signs'):
            app.start_app(input_method=lambda _: next(inputs), debug=True)


    def testAfterLoginWrongInput(self) -> None:
        pass
