import AuthLogin from "../pages/AuthLogin/AuthLogin.jsx";
import AuthRegister from "../pages/AuthRegister/AuthRegister.jsx";
import AuthReset from "../pages/AuthReset/AuthReset.jsx";
import Error from "../pages/Error/Error.jsx";
import Home from "../pages/Home/Home.jsx";
import ProtectedRoute from "./ProtectRoute.jsx";

import { BrowserRouter, Routes, Route } from "react-router-dom";

function Router() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AuthLogin />} />
          <Route path="/auth_reset" element={<AuthReset />} />
          <Route
            path="/auth_register"
            element={
              <ProtectedRoute>
                <AuthRegister />
              </ProtectedRoute>
            }
          />
          <Route
            path="/home"
            element={
              
                <Home />
              
            }
          />
          <Route path="*" element={<Error />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default Router;
