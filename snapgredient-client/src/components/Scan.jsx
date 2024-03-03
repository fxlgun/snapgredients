import "../styles/scan.css";
import UploadIconImg from "../public/upload-icon.png";
import RegularView from "../RegularView/RegularView";

const Scan = () => {
  function UploadOnClickFn() {
    console.log(document.getElementById("uploader"));
    const uploader = document.getElementById("uploader");
    if (uploader) {
      uploader.click();
    }
  }

  return (
    // <div className="FileUploaderMainContainer">
    //   <div className="FileUploaderContainer flex center">
    // <div
    //   className="FileUploaderBox flex column center"
    //   onClick={UploadOnClickFn}
    // >
    <RegularView />
    //   {/* //       <img
    // //         src={UploadIconImg}
    // //         alt="Upload Picture Image"
    // //         className="uploadIconImg"
    // //       /> */}
    // </div>
    //   </div>
    // </div>
  );
};

export default Scan;
