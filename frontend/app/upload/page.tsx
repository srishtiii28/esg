"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { BrainCircuit, Loader2, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState(0);
  const { toast } = useToast();
  const router = useRouter();

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

    setIsAnalyzing(true);
    
    try {
      console.log("File to upload:", {
        name: file.name,
        size: file.size,
        type: file.type
      });

      const formData = new FormData();
      formData.append("file", file);
      
      // Send file to analysis endpoint
      const response = await fetch("http://localhost:8003/analyze", {
        method: "POST",
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      });

      console.log("Response status:", response.status);
      
      if (!response.ok) {
        try {
          const errorData = await response.json();
          const errorMessage = errorData.detail || "Analysis failed";
          console.error("Error response:", errorData);
          throw new Error(errorMessage);
        } catch (parseError) {
          // If we can't parse the error response as JSON, just use the status text
          const errorMessage = response.statusText || "Analysis failed";
          console.error("Error response (non-JSON):", {
            status: response.status,
            statusText: response.statusText
          });
          throw new Error(errorMessage);
        }
      }

      const data = await response.json();
      console.log("Analysis Result:", data);
      
      // Store the analysis result in localStorage
      localStorage.setItem('esgAnalysisResult', JSON.stringify(data));
      
      // Redirect to dashboard
      router.push(`/dashboard/${data.report_hash}`);
    } catch (error) {
      console.error("Error:", error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to analyze report. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black to-gray-900">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-green-500 mb-4">
              Upload Your ESG Report
            </h1>
            <p className="text-muted-foreground">
              Upload your ESG report and let our AI analyze it for ESG metrics and greenwashing detection.
            </p>
          </div>

          {isAnalyzing ? (
            <div className="flex justify-center items-center h-screen">
              <div className="flex flex-col items-center gap-4 p-8">
                <Loader2 className="h-16 w-16 animate-spin text-green-500" />
                <div className="space-y-4">
                  <h2 className="text-2xl font-bold text-green-500">Analyzing Report...</h2>
                  <p className="text-center text-gray-400">
                    Our AI is processing your ESG report through multiple stages:
                  </p>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="text-gray-400">1. Text Extraction</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="text-gray-400">2. ESG Analysis</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="text-gray-400">3. Greenwashing Detection</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="text-gray-400">4. Report Summarization</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="text-gray-400">5. Blockchain Verification</span>
                    </div>
                  </div>
                  <div className="mt-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-24 h-1 bg-gray-700 rounded-full">
                        <div className="h-full bg-green-500 rounded-full transition-all duration-300" style={{ width: `${(analysisProgress / 5) * 100}%` }}></div>
                      </div>
                      <span className="text-yellow-400 font-medium">{analysisProgress}%</span>
                    </div>
                  </div>
                  <p className="text-center text-gray-400 mt-2">
                    Estimated time remaining: {estimatedTime} minutes
                  </p>
                  <p className="text-center text-gray-400 mt-4">
                    This process may take longer for larger reports. Please do not close this page.
                  </p>
                </div>
              </div>
            </div>
          ) : (
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
                    <Button
                      variant="outline"
                      onClick={async () => {
                        try {
                          const response = await fetch('/samples/sample-esg-report.txt');
                          const text = await response.text();
                          const blob = new Blob([text], { type: 'text/plain' });
                          const sampleFile = new File([blob], 'sample-esg-report.txt', { type: 'text/plain' });
                          setFile(sampleFile as File);
                        } catch (error) {
                          toast({
                            title: "Error",
                            description: "Failed to load sample report",
                            variant: "destructive",
                          });
                        }
                      }}
                      disabled={isAnalyzing}
                      className="glass bg-background/50 border border-green-500/20 hover:bg-green-500/30"
                    >
                      Use Sample Report
                    </Button>
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
          )}

          <div className="mt-8 text-center text-muted-foreground">
            <p>
              Your report will be analyzed using our AI models and the results will be securely stored on the EduChain Testnet.
            </p>
            <p className="mt-2">
              Supported formats: PDF, DOC, DOCX, TXT
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
