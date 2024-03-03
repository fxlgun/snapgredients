import Navbar from "./components/Navbar";
import "./styles/loading.css";

const Loading = () => {
  return (
    <div>
      <marquee direction="down">
        <Navbar />
      </marquee>
    </div>
  );
};

export default Loading;
