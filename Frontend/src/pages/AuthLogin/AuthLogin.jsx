import CardLogin from "../../Components/CardLogin/CardLogin";
import Btn from "../../Components/Button/Btn";
import InputForm from "../../Components/Input/InputForm";
import Notifications from "../../Components/Notification/Notifications.jsx";
import iconCpf from "../../assets/img/User.svg";
import iconSenha from "../../assets/img/Password.svg";
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { cpfMask } from "../../utils/mask.js";
import { transformRequest } from "../../utils/transformRequest.js";
import { ClipLoader } from "react-spinners";

function AuthLogin() {
  const [rawValue, setRawValue] = useState("");
  const [passwordValue, setPasswordValue] = useState("");
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const savedNotification = localStorage.getItem("notification");
    if (savedNotification) {
      setNotification(JSON.parse(savedNotification));
      localStorage.removeItem("notification");
    }
  }, []);

  const handleChange = (event) => {
    const value = event.target.value;
    const numericValue = value.replace(/\D/g, "");
    const maskedValue = cpfMask(numericValue);
    setRawValue(maskedValue);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (loading) return;
    setLoading(true);
    try {
      const data = await transformRequest("/api/v1/auth_login/", "POST", {
        cpf: rawValue,
        password: passwordValue,
      });
      if (data.auth_login === "auth_register") {
        localStorage.setItem("access", JSON.stringify(data.access));
        localStorage.setItem("refresh", JSON.stringify(data.refresh));
        window.location.href = "/auth_register";
      } else if (data.auth_login === "access") {
        localStorage.setItem("access", JSON.stringify(data.access));
        localStorage.setItem("refresh", JSON.stringify(data.refresh));
        window.location.href = "/home";
      }
    } catch (error) {
      localStorage.setItem(
        "notification",
        JSON.stringify({
          color: "danger",
          text: "CPF ou senha incorretos. Por favor, tente novamente",
        })
      );
      window.location.reload();
    }
    setLoading(false);
  };

  return (
    <>
      {notification && (
        <Notifications color={notification.color} text={notification.text} />
      )}
      <form
        onSubmit={handleSubmit}
        className="flex justify-center items-center h-screen mx-[10vw]"
      >
        <CardLogin title="IaEco">
          <InputForm
            user={iconCpf}
            forLabel="cpfInput"
            textLabel="CPF"
            id="cpfInput"
            type="text"
            classe={"hidden"}
            placeholder="000.000.000-00"
            width="w-full"
            height="h-[2.5rem]"
            valueInput={rawValue}
            nameInput="cpf"
            maxLength="14"
            onChange={handleChange}
          />
          <InputForm
            user={iconSenha}
            forLabel="senha"
            textLabel="SENHA"
            id="senha"
            type="password"
            placeholder="••••••••••••••••"
            width="w-full"
            height="h-[2.5rem]"
            nameInput="password"
            classe={"cursor-pointer"}
            onChange={(e) => setPasswordValue(e.target.value)}
          />
          <Btn
            id="authLogin"
            nameBtn={loading ? <ClipLoader color="#fff" size={20} /> : "Login"}
            width="w-full"
            height="h-[3.8rem]"
            disabled={loading}
            className="
                    bg-primary
                    hover:bg-primary-hover
                    focus:outline-primary-hover
                    active:bg-primary-hover"
          />
          <Link
            to="/auth_reset"
            className="w-full flex mt-3 font-[var(--font-primary)] font-bold underline underline-offset-2 decoration-1 cursor-pointer hover:text-[var(--color-gray-3)] content-center justify-end"
          >
            Esqueci minha senha?
          </Link>
        </CardLogin>
      </form>
    </>
  );
}

export default AuthLogin;
