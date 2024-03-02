import React, { useEffect, useRef, useState } from "react";

import * as LR from "@uploadcare/blocks";
import blocksStyles from "@uploadcare/blocks/web/lr-file-uploader-regular.min.css?url";
import { OutputFileEntry } from "@uploadcare/blocks";

import st from "./RegularView.module.css";
import axios from 'axios';


LR.registerBlocks(LR);

const sendPic = async (url) => {
  try {
    // Fetch image from CDN
    const imageData = await fetchImageFromCDN(url);

    // Send image data to the server
    await sendImageToServer(imageData);
  } catch (error) {
    console.error('An unexpected error occurred:', error.message);
  }
  console.log(url);

}

async function fetchImageFromCDN(cdnUrl) {
  
  try {
    const response = await axios.get(cdnUrl, { responseType: 'arraybuffer' });
    return response.data;
  } catch (error) {
    console.error('Error fetching image from CDN:', error.message);
    throw error;
  }
}

async function sendImageToServer(imageData) {
  const serverEndpoint = 'https://localhost:8000'; //change this with actual url
  
  try {
    const response = await axios.post(serverEndpoint, { imageData });
    console.log('Image sent successfully:', response.data);
  } catch (error) {
    console.error('Error sending image to the server:', error.message);
  }
}

export default function RegularView() {
  const [files, setFiles] = useState<OutputFileEntry<"success">[]>([]);
  const ctxProviderRef = useRef<InstanceType<LR.UploadCtxProvider>>(null);

  useEffect(() => {
    const ctxProvider = ctxProviderRef.current;
    if (!ctxProvider) return;

    const handleChangeEvent = (e: LR.EventMap["change"]) => {
      console.log("change event payload:", e);

      setFiles([
        ...e.detail.allEntries.filter((f) => f.status === "success"),
      ] as OutputFileEntry<"success">[]);
    };

    /*
      Note: Event binding is the main way to get data and other info from File Uploader.
      There plenty of events you may use.

      See more: https://uploadcare.com/docs/file-uploader/events/
     */
    ctxProvider.addEventListener("change", handleChangeEvent);
    return () => {
      ctxProvider.removeEventListener("change", handleChangeEvent);
    };
  }, [setFiles]);

  return (
    <div>
      <lr-config
        ctx-name="my-uploader"
        pubkey="2b7f257e8ea0817ba746"
        sourceList="local, url, camera"
        multiple={false}
      ></lr-config>
      <lr-file-uploader-regular
        ctx-name="my-uploader"
        css-src={blocksStyles}/>
      <lr-upload-ctx-provider
        ctx-name="my-uploader"
        ref={ctxProviderRef}
      ></lr-upload-ctx-provider>

      <div className={st.previews}>
        {files.map((file) => (
          <div key={file.uuid} className={st.previewWrapper}>
            <img
              className={st.previewImage}
              key={file.uuid}
              src={`${file.cdnUrl}/-/preview/-/resize/x400/`}
              width="200"
              height="200"
              alt={file.fileInfo.originalFilename || ""}
              title={file.fileInfo.originalFilename || ""}
            />

            <p className={st.previewData}>{file.fileInfo.originalFilename}</p>
            <p className={st.previewData}>{formatSize(file.fileInfo.size)}</p>
          </div>
        ))}
      </div>

      <button id="start-button" styles={{width: 200, height: 35, color: "lightgrey",}} onClick={() => sendPic(files[0]['cdnUrl'])}>
        Start
      </button>
    </div>
  );
}

function formatSize(bytes: number | null) {
  if (!bytes) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / k ** i).toFixed(2))} ${sizes[i]}`;
}
