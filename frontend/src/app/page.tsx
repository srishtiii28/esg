"use client";

import { useState } from 'react';
import Image from 'next/image';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  const [error, setError] = useState<string | null>(null);

  const API_URL = 'http://127.0.0.1:8000';

  const checkApiStatus = async () => {
    try {
      const response = await fetch(API_URL);
      return response.ok;
    } catch {
      return false;
    }
  };

  const analyzeReport = async () => {
    if (!file) return;

    setAnalyzing(true);
    setError(null);

    try {
      // Check API status first
      const isApiUp = await checkApiStatus();
      if (!isApiUp) {
        throw new Error('API server is not responding. Please check if the backend server is running.');
      }

      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
        mode: 'cors',
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Server error (${response.status}): ${errorText || 'No error details available'}`
        );
      }

      const data = await response.json();
      if (!data) {
        throw new Error('Received empty response from server');
      }

      setResults(data);
    } catch (error) {
      console.error('Error analyzing report:', error);
      setError(
        error instanceof Error
          ? error.message
          : 'Failed to analyze report. Please try again.'
      );
      setResults(null);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-green-600 dark:text-green-400">GreenStamp</h1>
          <p className="text-gray-600 dark:text-gray-300">AI + Blockchain-powered ESG Analysis</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Upload Section */}
        <section className="mb-12 bg-white dark:bg-gray-800 rounded-lg p-8 shadow-lg">
          <h2 className="text-2xl font-semibold mb-4 dark:text-white">Analyze ESG Report</h2>
          <div className="flex flex-col items-center gap-4">
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileUpload}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
            />
            <button
              onClick={analyzeReport}
              disabled={!file || analyzing}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {analyzing ? 'Analyzing...' : 'Analyze Report'}
            </button>
          </div>
        </section>

        {/* Error Message */}
        {error && (
          <div className="mb-8 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Results Section */}
        {results && (
          <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* ESG Scores */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
              <h3 className="text-xl font-semibold mb-4 dark:text-white">ESG Scores</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-300">Environmental</span>
                  <span className="text-green-600 font-bold">
                    {results?.environmental ? Math.round(results.environmental * 100) : 'N/A'}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-300">Social</span>
                  <span className="text-green-600 font-bold">
                    {results?.social ? Math.round(results.social * 100) : 'N/A'}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-300">Governance</span>
                  <span className="text-green-600 font-bold">
                    {results?.governance ? Math.round(results.governance * 100) : 'N/A'}%
                  </span>
                </div>
                <div className="pt-4 border-t">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-800 dark:text-white font-semibold">Total Score</span>
                    <span className="text-green-600 font-bold text-xl">
                      {results?.total ? Math.round(results.total * 100) : 'N/A'}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Blockchain Verification */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
              <h3 className="text-xl font-semibold mb-4 dark:text-white">Blockchain Verification</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-600 dark:text-gray-300">Report Hash</label>
                  <code className="block mt-1 p-2 bg-gray-100 dark:bg-gray-700 rounded text-sm font-mono break-all">
                    {results.report_hash}
                  </code>
                </div>
                {results.ipfs_url && (
                  <div>
                    <label className="block text-sm font-medium text-gray-600 dark:text-gray-300">IPFS URL</label>
                    <code className="block mt-1 p-2 bg-gray-100 dark:bg-gray-700 rounded text-sm font-mono break-all">
                      {results.ipfs_url}
                    </code>
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {/* Features Grid */}
        <section className="mt-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* AI Analysis */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
              <div className="text-green-600 dark:text-green-400 text-2xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold mb-2 dark:text-white">AI-Powered Analysis</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Advanced NLP models analyze ESG reports for comprehensive scoring and greenwashing detection.
              </p>
            </div>

            {/* Blockchain Verification */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
              <div className="text-green-600 dark:text-green-300 text-2xl mb-4">
                ⛓️ Blockchain Verified
              </div>
              <h3 className="text-xl font-semibold mb-2 dark:text-white">
                Tamper-Proof Storage
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Reports and scores are stored on Polygon blockchain and IPFS for transparency and verification.
              </p>
            </div>

            {/* Data Insights */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
              <div className="text-green-600 dark:text-green-400 text-2xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2 dark:text-white">Data Insights</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Comprehensive analytics and visualizations of ESG performance metrics and trends.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}