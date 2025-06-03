import CardLogin from "../../Components/CardLogin/CardLogin";
import Btn from "../../Components/Button/Btn";
import InputForm from "../../Components/Input/InputForm";
import Notifications from "../../Components/Notification/Notifications.jsx";
import iconCpf from "../../assets/img/User.svg";
import iconSenha from "../../assets/img/Password.svg";
import Refresh from "../../assets/img/Refresh.svg";
import React, { useState, useEffect } from "react";
import { cpfMask } from "../../utils/mask.js";
import { transformRequest } from "../../utils/transformRequest.js";
import { ClipLoader } from "react-spinners";

function AuthReset() {
  const [rawValue, setRawValue] = useState("");
  const [captchaValue, setCaptchaValue] = useState("");
  const [captchaImage, setCaptchaImage] = useState("");
  const [captchaKey, setCaptchaKey] = useState("");
  const [reloadCaptcha, setReloadCaptcha] = useState(false);
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const savedNotification = localStorage.getItem("notification");
    if (savedNotification) {
      setNotification(JSON.parse(savedNotification));
      localStorage.removeItem("notification");
    }
  }, []);

  useEffect(() => {
    transformRequest("/api/v1/api/captcha/", "GET").then((data) => {
      setCaptchaImage(import.meta.env.VITE_API_URL + data.captcha_image);
      setCaptchaKey(data.captcha_key);
    });
  }, [reloadCaptcha]);

  const handleReloadCaptcha = () => {
    setReloadCaptcha((prev) => !prev);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (loading) return;
    setLoading(true);
    if (!rawValue || !captchaValue) {
      localStorage.setItem(
        "notification",
        JSON.stringify({
          color: "danger",
          text: "Por favor, preencha todos os campos.",
        })
      );
      return;
    }
    try {
      const data = await transformRequest(
        "/api/v1/api/validate-captcha/",
        "POST",
        {
          captcha_key: captchaKey,
          captcha_value: captchaValue,
        }
      );
      if (data.message === "Captcha válido") {
        try {
          await transformRequest("/api/v1/auth_reset/", "POST", {
            cpf: rawValue,
          }).then((data) => {
            localStorage.setItem(
              "notification",
              JSON.stringify({
                color: "success",
                text: "Nova senha enviada para o e-mail cadastrado.",
              })
            );
            window.location.href = "/";
          });
        } catch (error) {
          localStorage.setItem(
            "notification",
            JSON.stringify({
              color: "danger",
              text: "Cpf inválido. Tente novamente.",
            })
          );
          window.location.reload();
        }
      } else {
        console.log("reste");
      }
    } catch (error) {
      localStorage.setItem(
        "notification",
        JSON.stringify({
          color: "danger",
          text: "Captcha inválido. Tente novamente.",
        })
      );
      window.location.reload();
    }
    setLoading(false);
  };

  const handleChange = (event) => {
    const value = event.target.value;
    const numericValue = value.replace(/\D/g, "");
    const maskedValue = cpfMask(numericValue);
    setRawValue(maskedValue);
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
        <CardLogin
          title="Esqueci minha senha"
          subtitle="Para redefinir sua senha, digite o seu CPF"
        >
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
          <div className="input-form flex flex-row w-full h-[5rem] bg-[var(--color-gray)] justify-center content-start rounded-[0.5rem] my-[1.5rem] p-[0.5rem] gap-[1rem]">
            {captchaImage ? (
              <img
                className="w-[30rem] h-[4rem]"
                src={captchaImage}
                alt="captcha"
              />
            ) : null}
            <button
              className="cursor-pointer"
              type="button"
              onClick={handleReloadCaptcha}
            >
              <img className="w-[2rem]" src={Refresh} alt="image refresh" />
            </button>
          </div>
          <InputForm
            user={iconSenha}
            forLabel="textCaptcha"
            textLabel="REPETIR TEXTO ACIMA"
            id="textCaptcha"
            type="text"
            placeholder="••••••••••••••••"
            width="w-full"
            classe="hidden"
            height="h-[2.5rem]"
            nameInput={captchaValue}
            onChange={(e) => setCaptchaValue(e.target.value)}
          />
          <Btn
            id="authReset"
            nameBtn={loading ? <ClipLoader color="#fff" size={20} /> : "Enviar"}
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

export default AuthReset;
