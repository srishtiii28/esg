import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, XCircle, Fuel, Copy, ExternalLink } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

interface TransactionDetails {
  transaction_hash?: string;
  status?: number;
  gas_used?: number;
  token_ticker: string;
  approve_transaction_hash?: string;
  approve_status?: number;
  approve_gas_used?: number;
  sell_transaction_hash?: string;
  sell_status?: number;
  sell_gas_used?: number;
}

interface TransactionComponentProps {
  details: TransactionDetails;
}

export function TransactionComponent({ details }: TransactionComponentProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatGas = (gas: number) => {
    return new Intl.NumberFormat("en-US").format(gas);
  };

  const getStatusColor = (status: number) => {
    return status === 1
      ? "bg-green-500/20 text-green-500"
      : "bg-red-500/20 text-red-500";
  };

  const truncateHash = (hash: string) => {
    return `${hash.slice(0, 6)}...${hash.slice(-4)}`;
  };

  const isSellTransaction = details.approve_transaction_hash !== undefined;

  return (
    <Card className="glass-card">
      <CardContent className="pt-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              {isSellTransaction ? "Sell Transaction" : "Buy Transaction"} Details
              <Badge className={getStatusColor(isSellTransaction ? details.sell_status || 0 : details.status || 0)}>
                {isSellTransaction ? (details.sell_status === 1 ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />) : 
                 (details.status === 1 ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />)}
                {isSellTransaction ? (details.sell_status === 1 ? "Success" : "Failed") : 
                 (details.status === 1 ? "Success" : "Failed")}
              </Badge>
            </h3>
            <Badge variant="outline">{details.token_ticker}</Badge>
          </div>

          <div className="space-y-3">
            {isSellTransaction ? (
              <>
                <div className="flex items-center justify-between p-3 rounded-lg bg-gray-800/50">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400">Approve Transaction Hash</span>
                    <span className="font-mono">
                      {truncateHash(details.approve_transaction_hash || "")}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(details.approve_transaction_hash || "")}
                      className="h-8 w-8 p-0"
                    >
                      {copied ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() =>
                        window.open(
                          `https://edu-chain-testnet.blockscout.com/tx/0x${details.approve_transaction_hash}`,
                          "_blank"
                        )
                      }
                      className="h-8 w-8 p-0"
                    >
                      <ExternalLink className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="flex items-center gap-2 p-3 rounded-lg bg-gray-800/50">
                  <Fuel className="h-4 w-4 text-orange-500" />
                  <span className="text-gray-400">Approve Gas Used</span>
                  <span className="font-mono">
                    {formatGas(details.approve_gas_used || 0)} wei
                  </span>
                </div>

                <div className="flex items-center justify-between p-3 rounded-lg bg-gray-800/50">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400">Sell Transaction Hash</span>
                    <span className="font-mono">
                      {truncateHash(details.sell_transaction_hash || "")}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(details.sell_transaction_hash || "")}
                      className="h-8 w-8 p-0"
                    >
                      {copied ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() =>
                        window.open(
                          `https://edu-chain-testnet.blockscout.com/tx/0x${details.sell_transaction_hash}`,
                          "_blank"
                        )
                      }
                      className="h-8 w-8 p-0"
                    >
                      <ExternalLink className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="flex items-center gap-2 p-3 rounded-lg bg-gray-800/50">
                  <Fuel className="h-4 w-4 text-orange-500" />
                  <span className="text-gray-400">Sell Gas Used</span>
                  <span className="font-mono">
                    {formatGas(details.sell_gas_used || 0)} wei
                  </span>
                </div>
              </>
            ) : (
              <>
                <div className="flex items-center justify-between p-3 rounded-lg bg-gray-800/50">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400">Transaction Hash</span>
                    <span className="font-mono">
                      {truncateHash(details.transaction_hash || "")}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(details.transaction_hash || "")}
                      className="h-8 w-8 p-0"
                    >
                      {copied ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() =>
                        window.open(
                          `https://edu-chain-testnet.blockscout.com/tx/0x${details.transaction_hash}`,
                          "_blank"
                        )
                      }
                      className="h-8 w-8 p-0"
                    >
                      <ExternalLink className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="flex items-center gap-2 p-3 rounded-lg bg-gray-800/50">
                  <Fuel className="h-4 w-4 text-orange-500" />
                  <span className="text-gray-400">Gas Used</span>
                  <span className="font-mono">
                    {formatGas(details.gas_used || 0)} wei
                  </span>
                </div>
              </>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
