import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import NavBar from "../../Components/Navbar/Navbar";

test("Navbar has app name", () => {
    render(
        <MemoryRouter initialEntries={["/"]}>
            <NavBar />
        </MemoryRouter>
    );
    const linkElement = screen.getByText(/toEaseShifts/i);
    expect(linkElement).toBeInTheDocument();
});
