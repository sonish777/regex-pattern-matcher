import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import { RegexMatchAndReplacer } from "./pages";

const darkTheme = createTheme({
    palette: { mode: "dark" },
    typography: {
        fontFamily: '"Montserrat", serif'
    }
});

function App() {
    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <RegexMatchAndReplacer />
        </ThemeProvider>
    );
}

export default App;
