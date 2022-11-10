import { loadFeature, defineFeature } from "jest-cucumber";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
// eslint-disable-next-line no-unused-vars
import { BrowserRouter, MemoryRouter } from "react-router-dom";
import CreateSchedule from "../../../Pages/Schedule/CreateSchedule";
import "../../../locales/i18n";
import { act } from "react-dom/test-utils";
import setFormInputValue from "../../utils/setFormInputValue";
import mockAxios from "jest-mock-axios";

const feature = loadFeature(
    "src/tests/acceptance/features/generate_schedule.feature"
);

defineFeature(feature, (test) => {
    test("Start the creation of a new schedule in the Home page", ({
        given,
        when,
        then,
    }) => {
        given("I am logged in as a service manager", () => {
            // Login user storie not implemented yet
        });

        when("I am in the create schedule page", () => {
            render(
                <MemoryRouter initialEntries={["/schedule/create"]}>
                    <CreateSchedule />
                </MemoryRouter>
            );

            const element = screen.getAllByText("Criar Horário", {
                exact: false,
            });

            expect(element[0]).toBeInTheDocument();
            expect(element.length).toBe(2);
        });

        when("I insert the schedule name", () => {
            const name = screen.getByLabelText("Nome", { exact: false });
            act(() => {
                setFormInputValue(name, "schedule1");
                name.dispatchEvent(new Event("input", { bubbles: true }));
            });
        });

        when("I select month and year", () => {
            const date = screen.getByLabelText("Data", { exact: false });
            act(() => {
                setFormInputValue(date, "2022-12");
                date.dispatchEvent(new Event("input", { bubbles: true }));
            });
        });

        when(
            "I click on the button with the text 'Generate new schedule'",
            async () => {
                const user = userEvent.setup();
                const button = screen.getByText("Gerar Horário", {
                    exact: true,
                });
                await user.click(button);

                expect(mockAxios.post).toHaveBeenCalledTimes(1);
            }
        );

        then(
            "I should be presented with the text 'Request successfully submitted'",
            () => {
                const success = screen.getByText("a ser gerado", {
                    exact: false,
                });
                expect(success).toBeInTheDocument();
            }
        );
    });
});
