import CardLogin from "../../Components/CardLogin/CardLogin";
import Btn from "../../Components/Button/Btn";
import InputForm from "../../Components/Input/InputForm";
import Notifications from "../../Components/Notification/Notifications.jsx";
import iconCpf from "../../assets/img/User.svg";
import iconSenha from "../../assets/img/Password.svg";
import React, { useState, useEffect } from "react";
import { transformRequest } from "../../utils/transformRequest.js";
import { refreshAccessToken } from "../../services/auth.js";
import { ClipLoader } from "react-spinners";

function AuthRegister() {
  const [notification, setNotification] = useState(null);
  const [currentPassword, setCurrentPassword] = useState("");
  const [password, setPassword] = useState("");
  const [passwordRepet, setPasswordRepet] = useState("");
  const [hasMinLength, setHasMinLength] = useState(false);
  const [hasUppercase, setHasUppercase] = useState(false);
  const [hasLowercase, setHasLowercase] = useState(false);
  const [hasNumber, setHasNumber] = useState(false);
  const [hasSpecialChar, setHasSpecialChar] = useState(false);
  const [loading, setLoading] = useState(false);

  const validatePassword = (password) => {
    setHasMinLength(password.length >= 8);
    setHasUppercase(/[A-Z]/.test(password));
    setHasLowercase(/[a-z]/.test(password));
    setHasNumber(/\d/.test(password));
    setHasSpecialChar(/[!@#$%^&*(),.?":{}|<>]/.test(password));
  };

  useEffect(() => {
    const savedNotification = localStorage.getItem("notification");
    if (savedNotification) {
      setNotification(JSON.parse(savedNotification));
      setTimeout(() => localStorage.removeItem("notification"), 100);
    }
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (loading) return;
    setLoading(true);

    if (
      !hasMinLength ||
      !hasUppercase ||
      !hasLowercase ||
      !hasNumber ||
      !hasSpecialChar
    ) {
      localStorage.setItem(
        "notification",
        JSON.stringify({
          color: "danger",
          text: "Senha não contém os requisitos necessários.",
        })
      );
      window.location.reload();
    }
    if (!currentPassword || !password || !passwordRepet) {
      localStorage.setItem(
        "notification",
        JSON.stringify({
          color: "danger",
          text: "Por favor, preencha todos os campos.",
        })
      );
      window.location.reload();
    }
    if (password !== passwordRepet) {
      localStorage.setItem(
        "notification",
        JSON.stringify({
          color: "danger",
          text: "A nova senha não confere com a confirmação da senha.",
        })
      );
      window.location.reload();
    }
    try {
      const refresh = await refreshAccessToken();
      const data = await transformRequest(
        "/api/v1/change_password/",
        "POST",
        {
          old_password: currentPassword,
          new_password: password,
          confirm_password: passwordRepet,
        },
        refresh
      );
      if (data.status)
        localStorage.setItem(
          "notification",
          JSON.stringify({
            color: "success",
            text: "Senha Atualizada com sucesso.",
          })
        );
      window.location.href = "/";
    } catch (error) {
      localStorage.setItem(
        "notification",
        JSON.stringify({
          color: "danger",
          text: "A senha atual está incorreta.",
        })
      );
      console.error(error);
      window.location.reload();
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {notification && (
        <Notifications color={notification.color} text={notification.text} />
      )}
      <form
        onSubmit={handleSubmit}
        className="flex justify-center items-center h-screen mx-[7vw]"
      >
        <CardLogin
          title="Redefinir minha senha"
          subtitle="Para redefinir sua senha, digite a senha enviada por e-mail."
        >
          <InputForm
            user={iconCpf}
            forLabel="password"
            textLabel="SENHA ATUAL"
            id="password"
            type="password"
            placeholder="****************"
            width="w-full"
            classe=""
            height="h-[2.5rem]"
            nameInput="password"
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
          <InputForm
            user={iconSenha}
            forLabel="newPassword"
            textLabel="NOVA SENHA"
            id="newPassword"
            type="password"
            placeholder="••••••••••••••••"
            width="w-full"
            classe=""
            height="h-[2.5rem]"
            nameInput="newPassword"
            onChange={(e) => {
              setPassword(e.target.value);
              validatePassword(e.target.value);
            }}
          />
          <InputForm
            user={iconSenha}
            forLabel="repetPassword"
            textLabel="REPETIR SENHA"
            id="repetPassword"
            type="password"
            placeholder="••••••••••••••••"
            width="w-full"
            classe=""
            height="h-[2.5rem]"
            nameInput="repetPassword"
            onChange={(e) => setPasswordRepet(e.target.value)}
          />
          <p className="text-[var(--color-gray-3)]">A senha deve conter:</p>
          <ul className="text-[var(--color-gray-3)] ml-3 mb-3 list-inside list-disc">
            <li className={hasMinLength ? "text-green-500" : "text-red-500"}>
              No mínimo 8 caracteres
            </li>
            <li className={hasUppercase ? "text-green-500" : "text-red-500"}>
              Uma letra maiúscula
            </li>
            <li className={hasLowercase ? "text-green-500" : "text-red-500"}>
              Uma minúscula
            </li>
            <li className={hasNumber ? "text-green-500" : "text-red-500"}>
              Um Número
            </li>
            <li className={hasSpecialChar ? "text-green-500" : "text-red-500"}>
              Um caractere especial.
            </li>
          </ul>
          <Btn
            id="authRegister"
            nameBtn={
              loading ? (
                <ClipLoader color="#fff" size={20} />
              ) : (
                "Redefinir Senha"
              )
            }
            width="w-full"
            height="h-[3.8rem]"
            disabled={loading}
            className="
                    bg-primary
                    hover:bg-primary-hover
                    focus:outline-primary-hover
                    active:bg-primary-hover"
          />
        </CardLogin>
      </form>
    </>
  );
}

export default AuthRegister;
