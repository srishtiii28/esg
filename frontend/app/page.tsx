import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  BrainCircuit,
  MessageSquare,
  Search,
  Twitter,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/navbar";
import Image from "next/image";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">
                    ESG Analysis Platform{" "}
                    <span className="text-green-500">Powered by AI & Blockchain</span>
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    GreenStamp uses advanced AI and blockchain technology to provide comprehensive ESG analysis, greenwashing detection, and secure report verification.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Button
                    size="lg"
                    className="bg-green-500/20 hover:bg-green-500/30 text-white group transition-all duration-300 ease-in-out"
                    asChild
                  >
                    <Link href="/upload">
                      Analyze Report
                      <ArrowRight className="ml-2 h-4 w-4 transition-transform duration-300 ease-in-out group-hover:translate-x-1" />
                    </Link>
                  </Button>
                  <Button variant="outline" size="lg" className="border-green-500/20">
                    Learn More
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative h-[450px] w-full overflow-hidden rounded-xl glass p-4">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-full max-w-md space-y-4 rounded-lg glass-card p-6">
                      <div className="space-y-2">
                        <h3 className="text-xl font-bold text-green-500">
                          ESG Report Analysis
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          Upload your ESG report to get instant analysis
                        </p>
                      </div>
                      <div className="space-y-4">
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                              <BrainCircuit className="h-4 w-4 text-green-500" />
                              <span className="text-sm font-medium">
                                AI Analysis
                              </span>
                            </div>
                            <span className="text-sm font-medium text-green-500">
                              Complete
                            </span>
                          </div>
                          <div className="h-2 w-full rounded-full bg-muted">
                            <div className="h-full w-full rounded-full bg-green-500" />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                              <BarChart3 className="h-4 w-4 text-green-500" />
                              <span className="text-sm font-medium">
                                Blockchain Verification
                              </span>
                            </div>
                            <span className="text-sm font-medium text-green-500">
                              Secure
                            </span>
                          </div>
                          <div className="h-2 w-full rounded-full bg-muted">
                            <div className="h-full w-full rounded-full bg-green-500" />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                              <MessageSquare className="h-4 w-4 text-green-500" />
                              <span className="text-sm font-medium">
                                Greenwashing Detection
                              </span>
                            </div>
                            <span className="text-sm font-medium text-green-500">
                              Advanced
                            </span>
                          </div>
                          <div className="h-2 w-full rounded-full bg-muted">
                            <div className="h-full w-full rounded-full bg-green-500" />
                          </div>
                        </div>
                      </div>
                      <div className="rounded-lg bg-gradient-to-r from-green-500/10 to-yellow-500/10 p-3 border border-green-500/20">
                        <p className="text-sm">
                          <strong className="text-yellow-500">
                            Platform Features:
                          </strong>{" "}
                          AI-powered ESG scoring, blockchain-based verification, and comprehensive report analysis.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg glass px-3 py-1 text-sm neon-border">
                  Features
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                  Comprehensive ESG Analysis
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Our platform combines advanced AI with blockchain technology to provide you with reliable and verifiable ESG insights.
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 md:grid-cols-2 lg:grid-cols-3">
              <div className="flex flex-col items-center space-y-4 rounded-lg glass-card p-6 neon-border">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/20">
                  <BrainCircuit className="h-8 w-8 text-primary" />
                </div>
                <h3 className="text-xl font-bold text-green-500">
                  AI-Powered Analysis
                </h3>
                <p className="text-center text-muted-foreground">
                  Advanced NLP models analyze ESG reports for comprehensive scoring and greenwashing detection.
                </p>
              </div>
              <div className="flex flex-col items-center space-y-4 rounded-lg glass-card p-6">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-yellow-500/20">
                  <BarChart3 className="h-8 w-8 text-yellow-500" />
                </div>
                <h3 className="text-xl font-bold text-yellow-500">
                  Blockchain Verification
                </h3>
                <p className="text-center text-muted-foreground">
                  Reports and scores are stored on Polygon blockchain and IPFS for transparency and verification.
                </p>
              </div>
              <div className="flex flex-col items-center space-y-4 rounded-lg glass-card p-6">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-500/20">
                  <MessageSquare className="h-8 w-8 text-green-500" />
                </div>
                <h3 className="text-xl font-bold text-green-500">
                  Data Insights
                </h3>
                <p className="text-center text-muted-foreground">
                  Comprehensive analytics and visualizations of ESG performance metrics and trends.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section id="how-it-works" className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg glass px-3 py-1 text-sm border-yellow-500/20">
                  Process
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                  How <span className="text-green-500">GreenStamp</span> Works
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Our transparent process helps you understand exactly how we analyze and verify ESG reports.
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl grid-cols-1 gap-8 py-12 md:grid-cols-2">
              <div className="flex flex-col space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-yellow-500/20 text-white">
                    <span className="h-4 w-10 text-center text-sm leading-none">
                      1
                    </span>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold text-yellow-500">
                      Document Upload
                    </h3>
                    <p className="text-muted-foreground">
                      Upload your ESG report in any format - PDF, DOCX, or text.
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-500/20 text-white">
                    <span className="h-4 w-10 text-center text-sm leading-none">
                      2
                    </span>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold text-green-500">
                      AI Analysis
                    </h3>
                    <p className="text-muted-foreground">
                      Our AI models analyze the content for ESG metrics and greenwashing indicators.
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-yellow-500/20 text-white">
                    <span className="h-4 w-10 text-center text-sm leading-none">
                      3
                    </span>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold text-yellow-500">
                      Blockchain Verification
                    </h3>
                    <p className="text-muted-foreground">
                      Reports and scores are securely stored on the Polygon blockchain.
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-y-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-green-500/20 to-yellow-500/20 text-white">
                    <span className="h-4 w-10 text-center text-sm leading-none">
                      4
                    </span>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold text-gradient-to-r from-green-500 to-yellow-500">
                      Report Access
                    </h3>
                    <p className="text-muted-foreground">
                      Access your verified reports and analysis results anytime.
                    </p>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative h-[450px] w-full overflow-hidden rounded-xl glass p-4">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Image
                      width={400}
                      height={400}
                      src="/placeholder.svg?height=400&width=400"
                      alt="ESG Analysis Process Visualization"
                      className="rounded-lg shadow-lg neon-border"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>



        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">
                  Ready to Enhance Your ESG Analysis?
                </h2>
                <p className="max-w-[600px] text-muted-foreground md:text-xl">
                  Join organizations using AI-powered insights and blockchain verification to build sustainable business practices.
                </p>
              </div>
              <div className="flex flex-col gap-2 min-[400px]:flex-row">
                <Button
                  size="lg"
                  className="bg-primary hover:bg-primary/80 neon-glow group transition-all duration-300 ease-in-out"
                  asChild
                >
                  <Link href="/login">
                    Get Started
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform duration-300 ease-in-out group-hover:translate-x-1" />
                  </Link>
                </Button>
                <Button variant="outline" size="lg" className="neon-border">
                  View Demo
                </Button>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="w-full glass py-6 md:py-0 border-t border-green-500/20">
        <div className="container flex items-center justify-between gap-4 md:h-24">
          <div className="flex items-center space-x-4">
            <Link
              href="#"
              className="text-sm text-muted-foreground underline-offset-4 hover:text-green-500"
            >
              Terms
            </Link>
            <Link
              href="#"
              className="text-sm text-muted-foreground underline-offset-4 hover:text-green-500"
            >
              Privacy
            </Link>
            <Link
              href="#"
              className="text-sm text-muted-foreground underline-offset-4 hover:text-green-500"
            >
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
