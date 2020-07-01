import pytest
import fault as f
import magma as m
import shutil


def test_basic_assert():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8])) + m.ClockIO()
        io.O @= m.Register(T=m.Bits[8])()(io.I)
        f.assert_(io.I | f.implies | f.delay[1] | io.O, on=f.posedge(io.CLK))

    if shutil.which("ncsim"):
        tester = f.SynchronousTester(Main, Main.CLK)
        tester.circuit.I = 1
        tester.advance_cycle()
        tester.circuit.O.expect(1)
        tester.circuit.I = 0
        tester.advance_cycle()
        tester.circuit.O.expect(0)
        tester.advance_cycle()
        tester.circuit.I = 1
        tester.circuit.O.expect(0)
        tester.advance_cycle()
        tester.circuit.I = 0
        tester.circuit.O.expect(1)
        tester.advance_cycle()
        tester.circuit.O.expect(0)
        tester.compile_and_run("system-verilog", simulator="ncsim", flags=["-sv"])


@pytest.mark.xfail
def test_basic_assert_fail():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8])) + m.ClockIO()
        io.O @= m.Register(T=m.Bits[8])()(io.I)
        f.assert_(io.I | f.implies | f.delay[1] | ~io.O, on=f.posedge(io.CLK))

    if shutil.which("ncsim"):
        tester = f.SynchronousTester(Main, Main.CLK)
        tester.circuit.I = 1
        tester.advance_cycle()
        tester.circuit.I = 0
        tester.advance_cycle()
        tester.advance_cycle()
        tester.compile_and_run("system-verilog", simulator="ncsim", flags=["-sv"])
