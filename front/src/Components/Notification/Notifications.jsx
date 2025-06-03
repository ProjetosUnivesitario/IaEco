import "../../App.css";

function Notifications({ color, text }) {
  const removeAlert = () => {
    const alert = document.getElementById("alert");
    alert.remove();
  };

  return (
    <>
      <div
        id="alert"
        className={`w-auto h-fit flex justify-between items-center p-[1rem] rounded-[0.5rem] absolute text-[1.5rem] mt-6 alert-${color} shadow-xs notification-edit`}
      >
        <p className="mr-2">{text}</p>
        <button
          className="text-[var(--back)] text-[2rem] hover:border border-[var(--color-gray)] w-[3rem] h-[3rem] rounded-[0.5rem] shadow-xs"
          onClick={removeAlert}
        >
          X
        </button>
      </div>
    </>
  );
}

export default Notifications;
