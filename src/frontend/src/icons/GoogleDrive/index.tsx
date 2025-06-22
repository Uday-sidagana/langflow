import React, { forwardRef } from "react";
import GoogleDriveIconSVG from "./GoogleDrive.jsx";

export const GOOGLEDRIVEIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <GoogleDriveIconSVG ref={ref} {...props} />;
});