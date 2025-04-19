"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { BrainCircuit, File, Loader2, ArrowRight } from "lucide-react";
import { useAccount } from "wagmi";
import { useRouter } from "next/navigation";
import { Navbar } from "@/components/navbar";
import { Toaster } from "@/components/ui/toaster";

export default function UploadPage() {
  const { address } = useAccount();
  const [file, setFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const router = useRouter();
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      toast({
        title: "Error",
        description: "Please select a file to upload",
        variant: "destructive",
      });
      return;
    }

    if (!address) {
      toast({
        title: "Error",
        description: "Please connect your wallet to proceed",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    try {
      // TODO: Implement actual file upload and analysis
      toast({
        title: "Analysis Started",
        description: "Your ESG report is being analyzed. This may take a few minutes.",
      });
      // Simulate analysis
      await new Promise((resolve) => setTimeout(resolve, 2000));
      router.push("/dashboard");
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to analyze report. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <Toaster />
      <main className="flex-1 flex items-center justify-center py-12">
        <div className="w-full max-w-2xl space-y-8 px-4">
          <div className="space-y-2 text-center">
            <h1 className="text-3xl font-bold tracking-tighter">
              Upload Your ESG Report
            </h1>
            <p className="text-muted-foreground">
              Upload your ESG report and let our AI analyze it for ESG metrics and greenwashing detection.
            </p>
          </div>

          <div className="glass bg-background/50 p-6 rounded-xl border border-green-500/20 shadow-lg hover:shadow-xl transition-all duration-300 ease-in-out">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-4">
                <Label htmlFor="file">Select ESG Report</Label>
                <div className="flex items-center gap-4">
                  <Input
                    id="file"
                    type="file"
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileChange}
                    disabled={isAnalyzing}
                    className="glass bg-background/50 border border-green-500/20 focus:border-green-500/30 focus:ring-0 focus:outline-none focus:ring-green-500/20"
                  />
                  {file && (
                    <span className="text-sm text-muted-foreground">
                      Selected: {file.name}
                    </span>
                  )}
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-green-500 to-yellow-500 hover:from-green-600 hover:to-yellow-600 group transition-all duration-300 ease-in-out z-10"
                disabled={isAnalyzing || !file}
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    Analyze Report
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform duration-300 ease-in-out group-hover:translate-x-1" />
                  </>
                )}
              </Button>
            </form>
          </div>

          <div className="space-y-4">
            <h2 className="text-xl font-semibold">How It Works</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="glass bg-background/50 p-4 rounded-lg border border-green-500/20">
                <div className="flex items-center gap-2">
                  <BrainCircuit className="h-6 w-6 text-green-500" />
                  <span className="font-medium">AI Analysis</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                  Our AI analyzes your ESG report for compliance and metrics
                </p>
              </div>
              <div className="glass bg-background/50 p-4 rounded-lg border border-green-500/20">
                <div className="flex items-center gap-2">
                  <File className="h-6 w-6 text-green-500" />
                  <span className="font-medium">Report Verification</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                  Reports are verified and stored on the blockchain
                </p>
              </div>
              <div className="glass bg-background/50 p-4 rounded-lg border border-green-500/20">
                <div className="flex items-center gap-2">
                  <Loader2 className="h-6 w-6 text-green-500" />
                  <span className="font-medium">Real-time Insights</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                  Get instant insights and recommendations
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
