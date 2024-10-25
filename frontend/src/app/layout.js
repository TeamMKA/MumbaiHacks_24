import localFont from "next/font/local";
import "./globals.css";
import NavBar from "@components/NavBar";

export const metadata = {
  title: "SafeRakhshak",
  description: "CrowdSource Women Safety App",
};

const RootLayout = ({ children }) => {
  return (
    <html lang="en">
      <body>
       {/*  <Provider> */}

          <div className="main">
            <div className="gradient" />
          </div>

          <main className="app">
            <NavBar />
            {children}
          </main>
          
        {/* </Provider> */}
      </body>
    </html>
  );
};

export default RootLayout;