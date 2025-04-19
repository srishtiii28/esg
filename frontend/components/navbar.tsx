"use client";

import Link from "next/link";

import { ConnectButton } from "@rainbow-me/rainbowkit";
import { useAccount } from "wagmi";
import { useRouter } from "next/navigation";
export function Navbar() {
  const { address } = useAccount();
  const router = useRouter();
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full bg-gradient-to-r from-black to-green-900/50 glass">
      <div className="container flex h-16 items-center space-x-4 sm:justify-between sm:space-x-0">
        <div className="flex gap-6 md:gap-10">
          <Link href="/" className="inline-block font-bold text-green-500">
            GreenStamp
          </Link>
        </div>
        <div className="flex flex-1 items-center justify-end">
          <nav className="flex items-center space-x-6">
            {address && (
              <button
                onClick={() => router.push("/dashboard")}
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
              >
                Dashboard
              </button>
            )}
            <button
              onClick={() => scrollToSection("features")}
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
            >
              Features
            </button>
            <button
              onClick={() => scrollToSection("how-it-works")}
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
            >
              How It Works
            </button>
            <div className="ml-4">
              <ConnectButton.Custom>
                {({
                  account,
                  chain,
                  openAccountModal,
                  openChainModal,
                  openConnectModal,
                  mounted,
                }) => {
                  const ready = mounted;
                  const connected = ready && account && chain;

                  return (
                    <div
                      {...(!ready && {
                        "aria-hidden": true,
                        style: {
                          opacity: 0,
                          pointerEvents: "none",
                          userSelect: "none",
                        },
                      })}
                    >
                      {(() => {
                        if (!connected) {
                          return (
                            <button
                              onClick={openConnectModal}
                              type="button"
                              className="bg-gradient-to-r from-green-500/20 to-green-500/30 hover:from-green-500/30 hover:to-green-500/40 text-white inline-flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors border border-green-500/20"
                            >
                              Connect Wallet
                            </button>
                          );
                        }

                        return (
                          <div className="flex items-center gap-2">
                            <button
                              onClick={openChainModal}
                              type="button"
                              className="bg-primary/20 hover:bg-primary/30 text-primary inline-flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors neon-border"
                            >
                              {chain.hasIcon && (
                                <div className="rounded-full bg-white p-1">
                                  {chain.iconUrl && (
                                    <img
                                      alt={chain.name ?? ""}
                                      className="h-5 w-5 rounded-full"
                                      src={chain.iconUrl}
                                      onError={(e) => {
                                        if (e.target instanceof HTMLImageElement) {
                                          e.target.src = `https://raw.githubusercontent.com/rainbow-me/rainbowkit/main/packages/chains/src/resources/${chain.id}.png`;
                                        }
                                      }}
                                    />
                                  )}
                                </div>
                              )}
                              {chain.name}
                            </button>

                            <button
                              onClick={openAccountModal}
                              type="button"
                              className="bg-primary/20 hover:bg-primary/30 text-primary inline-flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors neon-border"
                            >
                              {account.displayName}
                              {account.displayBalance
                                ? ` (${account.displayBalance})`
                                : ""}
                            </button>
                          </div>
                        );
                      })()}
                    </div>
                  );
                }}
              </ConnectButton.Custom>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}
