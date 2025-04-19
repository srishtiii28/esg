"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { BrainCircuit, File, Loader2, BarChart3, CheckCircle2 } from "lucide-react";
import { useAccount } from "wagmi";

interface ESGAnalysis {
  environmental: number;
  social: number;
  governance: number;
  total: number;
  report_hash: string;
  ipfs_url: string | null;
  analysis: {
    scores: {
      environmental: number;
      social: number;
      governance: number;
      total: number;
    };
    category_details: {
      environmental: Record<string, number>;
      social: Record<string, number>;
      governance: Record<string, number>;
    };
    greenwashing_warnings: Array<{
      type: string;
      description: string;
      confidence: number;
      severity: string;
      text_snippet: string | null;
    }>;
    summary: {
      brief: string;
      full: string;
      length: number;
      compression_ratio: number;
    };
    text_excerpt: string;
    metadata: Record<string, string>;
  };
}

interface ESGReport {
  file: File;
  analysis: ESGAnalysis | null;
}

export default function DashboardPage() {
  const { address } = useAccount();
  const [reports, setReports] = useState<ESGReport[]>([]);
  const [loading, setLoading] = useState(false);
  const [verificationStatus, setVerificationStatus] = useState<any>(null);
  const { toast } = useToast();

  const fetchAnalysisData = async (report: ESGReport) => {
    setLoading(true);
    try {
      const storedResult = localStorage.getItem('esgAnalysisResult');
      if (!storedResult) {
        toast({
          title: "No Data",
          description: "Please upload and analyze an ESG report first",
          variant: "destructive",
        });
        setLoading(false);
        return;
      }

      const analysisData = JSON.parse(storedResult);
      setReports(prevReports => prevReports.map(r => r.file === report.file ? { ...r, analysis: analysisData } : r));

      // Update the page title with the report ID
      document.title = `ESG Report Analysis - ${analysisData.report_id}`;

      // Fetch blockchain verification status
      const verificationStatus = await fetchBlockchainVerification(analysisData.report_hash);
      setVerificationStatus(verificationStatus);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load analysis data",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchBlockchainVerification = async (reportHash: string) => {
    try {
      const response = await fetch(`https://alpha-scan-ai.vercel.app/api/verify/${reportHash}`);
      const data = await response.json();
      return data;
    } catch (error) {
      return { status: 'error', message: 'Failed to verify on blockchain' };
    }
  };

  const handleFileUpload = async (file: File) => {
    setReports(prevReports => [...prevReports, { file, analysis: null }]);
  };

  return (
    <div className="bg-black text-white min-h-screen">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-green-500 mb-2">
            Your ESG Analysis Dashboard
          </h1>
          <p className="text-gray-400">
            View your ESG report analysis results and EduChain Testnet verification status.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card className="bg-gray-800 p-6 border border-green-500/20">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-green-500">ESG Reports</h3>
                <Button
                  variant="outline"
                  onClick={() => handleFileUpload(new File([], 'example.txt', { type: 'text/plain' }))}
                  disabled={loading}
                  className="bg-green-500/20 hover:bg-green-500/30 text-white"
                >
                  {loading ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin text-white" />
                  ) : (
                    "Upload Report"
                  )}
                </Button>
              </div>

              {reports.map((report, index) => (
                <div key={index} className="space-y-4">
                  <h4 className="text-green-500 font-semibold mb-2">Report {index + 1}</h4>
                  {report.analysis ? (
                    <div className="space-y-4">
                      {/* Environmental Score */}
                      <span className="text-yellow-400 font-medium">{Math.round(analysisData.social * 100)}%</span>
                      <div className="w-24 h-1 bg-gray-700 rounded-full">
                        <div 
                          className="h-full bg-green-500 rounded-full transition-all duration-300"
                          style={{ width: `${analysisData.social * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Governance Score */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <BarChart3 className="h-4 w-4 text-green-500" />
                      <span className="text-green-500">Governance</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-yellow-400 font-medium">{Math.round(analysisData.governance * 100)}%</span>
                      <div className="w-24 h-1 bg-gray-700 rounded-full">
                        <div 
                          className="h-full bg-green-500 rounded-full transition-all duration-300"
                          style={{ width: `${analysisData.governance * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Total ESG Score */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <BarChart3 className="h-4 w-4 text-green-500" />
                      <span className="text-green-500">Total ESG Score</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-yellow-400 font-medium">{Math.round(analysisData.total * 100)}%</span>
                      <div className="w-24 h-1 bg-gray-700 rounded-full">
                        <div 
                          className="h-full bg-green-500 rounded-full transition-all duration-300"
                          style={{ width: `${analysisData.total * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Category Details */}
                  <div className="mt-4">
                    <h4 className="text-green-500 font-semibold mb-2">Category Details</h4>
                    <div className="space-y-2">
                      {Object.entries(analysisData.analysis.category_details).map(([category, details]) => (
                        <div key={category} className="space-y-1">
                          <h5 className="text-green-500 font-medium">{category.charAt(0).toUpperCase() + category.slice(1)}</h5>
                          <div className="space-y-1">
                            {Object.entries(details).map(([subcategory, score]) => (
                              <div key={subcategory} className="flex items-center justify-between">
                  <div className="flex items-center justify-between">
                    <span className="text-green-500">Blockchain Network</span>
                    <span className="text-yellow-400">EduChain Testnet</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-green-500">Transaction Hash</span>
                    <span className="text-yellow-400 font-mono text-sm">
                      {verificationStatus.txHash ? verificationStatus.txHash.slice(0, 10) + '...' : 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-green-500">Block Number</span>
                    <span className="text-yellow-400">{verificationStatus.blockNumber || 'N/A'}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-green-500">Timestamp</span>
                    <span className="text-yellow-400">{verificationStatus.timestamp ? new Date(verificationStatus.timestamp).toLocaleString() : 'N/A'}</span>
                  </div>

                  <div className="mt-4">
                    <h4 className="text-green-500 font-semibold mb-2">Greenwashing Risk</h4>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-green-500">Risk Level</span>
                        <span className={`text-${analysisData.analysis.greenwashing_warnings.length > 0 ? 'red-500' : 'green-500'} font-medium`}>
                          {analysisData.analysis.greenwashing_warnings.length > 0 ? 'High' : 'Low'}
                        </span>
                      </div>
                      {analysisData.analysis.greenwashing_warnings.length > 0 && (
                        <div className="mt-2">
                          <h5 className="text-green-500 font-medium mb-2">Warnings</h5>
                          <div className="space-y-2">
                            {analysisData.analysis.greenwashing_warnings.map((warning, index) => (
                              <div key={index} className="flex items-center space-x-2">
                                <span className="text-red-500">⚠️</span>
                                <div className="flex-1">
                                  <h6 className="font-medium">{warning.type}</h6>
                                  <p className="text-gray-400">{warning.description}</p>
                                  <p className="text-yellow-400 text-sm">Confidence: {Math.round(warning.confidence * 100)}%</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="mt-4">
                    <h4 className="text-green-500 font-semibold mb-2">Storage Details</h4>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-green-500">IPFS Storage</span>
                        <div className="flex items-center space-x-2">
                          <CheckCircle2 className="h-4 w-4 text-green-500" />
                          <span className="text-green-500 font-medium">Stored</span>
                        </div>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-green-500">Report Hash</span>
                        <span className="text-yellow-400 font-mono text-sm">{analysisData.report_hash.slice(0, 10)}...</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-green-500">IPFS URL</span>
                        <span className="text-yellow-400 font-mono text-sm">{analysisData.ipfs_url || 'Not available'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-400">No analysis data available</p>
              )}
            </div>
          </Card>
        </div>

        <div className="mt-8 text-center text-gray-400">
          <p>
            Your ESG analysis results are securely stored on the EduChain Testnet and can be verified at any time.
          </p>
        </div>
      </div>
    </div>
  );
}
