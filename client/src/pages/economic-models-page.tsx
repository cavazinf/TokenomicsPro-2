import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Textarea } from "@/components/ui/textarea";
import { 
  TrendingUp, 
  Coins, 
  BarChart as BarChartIcon, 
  PieChart, 
  DollarSign, 
  FileDown, 
  FileText,
  Info
} from 'lucide-react';

export default function Econometrics() {
  const [activeTab, setActiveTab] = useState("utility-token");
  const [simulationYears, setSimulationYears] = useState(5);
  const [simulationData, setSimulationData] = useState<any[]>([]);
  const [showResults, setShowResults] = useState(false);
  
  const [utilityTokenParams, setUtilityTokenParams] = useState({
    initialPrice: 1.0,
    initialSupply: 100000000,
    initialUsers: 10000,
    userGrowthRate: 15,
    utilityValue: 10,
    networkEffectFactor: 0.35,
    transactionVolumeFactor: 0.5,
    tokenVelocity: 5
  });

  const [securityTokenParams, setSecurityTokenParams] = useState({
    initialPrice: 10.0,
    initialSupply: 10000000,
    dividendYield: 5,
    marketGrowthRate: 12,
    riskPremium: 3,
    assetValue: 1000000,
    equityMultiple: 10
  });

  const [governanceTokenParams, setGovernanceTokenParams] = useState({
    initialPrice: 5.0,
    initialSupply: 50000000,
    initialStaking: 40,
    stakingReward: 8,
    votingRights: 1,
    networkValue: 5000000,
    governanceUtility: 20
  });

  const handleUtilityParamChange = (param: string, value: number) => {
    setUtilityTokenParams(prev => ({
      ...prev,
      [param]: value
    }));
  };

  const handleSecurityParamChange = (param: string, value: number) => {
    setSecurityTokenParams(prev => ({
      ...prev,
      [param]: value
    }));
  };

  const handleGovernanceParamChange = (param: string, value: number) => {
    setGovernanceTokenParams(prev => ({
      ...prev,
      [param]: value
    }));
  };

  const runSimulation = () => {
    // Simplified simulation logic based on model type
    let simulatedData = [];
    
    switch (activeTab) {
      case "utility-token":
        simulatedData = simulateUtilityToken();
        break;
      case "security-token":
        simulatedData = simulateSecurityToken();
        break;
      case "governance-token":
        simulatedData = simulateGovernanceToken();
        break;
    }
    
    setSimulationData(simulatedData);
    setShowResults(true);
  };

  const simulateUtilityToken = () => {
    const { initialPrice, initialSupply, initialUsers, userGrowthRate, 
            utilityValue, networkEffectFactor, transactionVolumeFactor, tokenVelocity } = utilityTokenParams;
    
    const data = [];
    let users = initialUsers;
    let price = initialPrice;
    let marketCap = initialPrice * initialSupply;
    let circulatingSupply = initialSupply * 0.2; // Assume 20% initial circulation
    let transactionVolume = initialUsers * utilityValue;
    
    for (let year = 0; year <= simulationYears; year++) {
      if (year > 0) {
        users = users * (1 + userGrowthRate / 100);
        const networkEffect = Math.pow(users / initialUsers, networkEffectFactor);
        transactionVolume = users * utilityValue * networkEffect;
        price = initialPrice * Math.pow(users / initialUsers, networkEffectFactor) * 
                Math.pow(transactionVolume / (initialUsers * utilityValue), transactionVolumeFactor);
        circulatingSupply = Math.min(initialSupply, circulatingSupply * (1 + 0.1)); // 10% more tokens circulate
        marketCap = price * circulatingSupply;
      }
      
      data.push({
        year,
        users: Math.round(users),
        price: parseFloat(price.toFixed(3)),
        circulatingSupply: Math.round(circulatingSupply),
        marketCap: Math.round(marketCap),
        transactionVolume: Math.round(transactionVolume),
        tokenVelocity: tokenVelocity,
      });
    }
    
    return data;
  };

  const simulateSecurityToken = () => {
    const { initialPrice, initialSupply, dividendYield, marketGrowthRate, 
            riskPremium, assetValue, equityMultiple } = securityTokenParams;
    
    const data = [];
    let price = initialPrice;
    let marketCap = initialPrice * initialSupply;
    let circulatingSupply = initialSupply * 0.3; // Assume 30% initial circulation
    let assetValueCurrent = assetValue;
    let dividendPerToken = (assetValue * (dividendYield / 100)) / initialSupply;
    
    for (let year = 0; year <= simulationYears; year++) {
      if (year > 0) {
        assetValueCurrent = assetValueCurrent * (1 + marketGrowthRate / 100);
        dividendPerToken = (assetValueCurrent * (dividendYield / 100)) / initialSupply;
        
        // Security token price is driven by dividends and growth expectations
        price = (dividendPerToken / (riskPremium / 100)) + 
                (initialPrice * Math.pow(1 + marketGrowthRate / 100, year / 2));
                
        circulatingSupply = Math.min(initialSupply, circulatingSupply * (1 + 0.1)); // 10% more tokens circulate
        marketCap = price * circulatingSupply;
      }
      
      data.push({
        year,
        price: parseFloat(price.toFixed(3)),
        circulatingSupply: Math.round(circulatingSupply),
        marketCap: Math.round(marketCap),
        assetValue: Math.round(assetValueCurrent),
        dividendPerToken: parseFloat(dividendPerToken.toFixed(4)),
        equityValue: Math.round(marketCap / equityMultiple),
      });
    }
    
    return data;
  };

  const simulateGovernanceToken = () => {
    const { initialPrice, initialSupply, initialStaking, stakingReward,
            votingRights, networkValue, governanceUtility } = governanceTokenParams;
    
    const data = [];
    let price = initialPrice;
    let marketCap = initialPrice * initialSupply;
    let circulatingSupply = initialSupply * 0.25; // Assume 25% initial circulation
    let stakedTokens = initialSupply * (initialStaking / 100);
    let networkValueCurrent = networkValue;
    let stakingYield = stakingReward;
    
    for (let year = 0; year <= simulationYears; year++) {
      if (year > 0) {
        networkValueCurrent = networkValueCurrent * (1 + 0.2); // 20% annual network growth
        
        const stakingRatio = stakedTokens / initialSupply;
        const governanceValue = governanceUtility * Math.log(1 + year);
        
        // Governance token price driven by network value, staking, and governance utility
        price = initialPrice * (networkValueCurrent / networkValue) * 
                (1 + (stakingRatio * stakingYield / 100)) *
                (1 + (governanceValue / 100));
                
        circulatingSupply = initialSupply - stakedTokens;
        stakedTokens = stakedTokens * (1 + 0.05); // 5% more tokens staked yearly
        stakedTokens = Math.min(stakedTokens, initialSupply * 0.9); // Max 90% staked
        marketCap = price * initialSupply;
      }
      
      data.push({
        year,
        price: parseFloat(price.toFixed(3)),
        circulatingSupply: Math.round(circulatingSupply),
        marketCap: Math.round(marketCap),
        stakedTokens: Math.round(stakedTokens),
        stakingRatio: parseFloat((stakedTokens / initialSupply * 100).toFixed(1)),
        networkValue: Math.round(networkValueCurrent),
        votingPower: Math.round(stakedTokens * votingRights),
      });
    }
    
    return data;
  };

  const resetSimulation = () => {
    setShowResults(false);
    setSimulationData([]);
  };

  const renderUtilityTokenForm = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="initialPrice">Initial Price (USD)</Label>
          <div className="flex items-center space-x-2">
            <span>$</span>
            <Input 
              id="initialPrice" 
              type="number" 
              min={0.001}
              step={0.1}
              value={utilityTokenParams.initialPrice}
              onChange={(e) => handleUtilityParamChange('initialPrice', parseFloat(e.target.value))}
            />
          </div>
          <p className="text-sm text-muted-foreground">Starting price of token</p>
        </div>
        <div className="space-y-2">
          <Label htmlFor="initialSupply">Initial Supply</Label>
          <Input 
            id="initialSupply" 
            type="number" 
            min={1000}
            step={1000}
            value={utilityTokenParams.initialSupply}
            onChange={(e) => handleUtilityParamChange('initialSupply', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">Total token supply</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="initialUsers">Initial Users</Label>
          <Input 
            id="initialUsers" 
            type="number" 
            min={100}
            step={100}
            value={utilityTokenParams.initialUsers}
            onChange={(e) => handleUtilityParamChange('initialUsers', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">Starting user base</p>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="userGrowthRate">User Growth Rate (%/year)</Label>
            <span>{utilityTokenParams.userGrowthRate}%</span>
          </div>
          <Slider
            id="userGrowthRate"
            min={0}
            max={100}
            step={1}
            value={[utilityTokenParams.userGrowthRate]}
            onValueChange={(value) => handleUtilityParamChange('userGrowthRate', value[0])}
          />
          <p className="text-sm text-muted-foreground">Annual user growth percentage</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="utilityValue">Utility Value per User</Label>
          <Input 
            id="utilityValue" 
            type="number" 
            min={1}
            step={1}
            value={utilityTokenParams.utilityValue}
            onChange={(e) => handleUtilityParamChange('utilityValue', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">Value created per user</p>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="networkEffectFactor">Network Effect Factor</Label>
            <span>{utilityTokenParams.networkEffectFactor}</span>
          </div>
          <Slider
            id="networkEffectFactor"
            min={0}
            max={1}
            step={0.01}
            value={[utilityTokenParams.networkEffectFactor]}
            onValueChange={(value) => handleUtilityParamChange('networkEffectFactor', value[0])}
          />
          <p className="text-sm text-muted-foreground">
            Strength of network effects (0-1)
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="transactionVolumeFactor">Transaction Volume Impact</Label>
            <span>{utilityTokenParams.transactionVolumeFactor}</span>
          </div>
          <Slider
            id="transactionVolumeFactor"
            min={0}
            max={1}
            step={0.01}
            value={[utilityTokenParams.transactionVolumeFactor]}
            onValueChange={(value) => handleUtilityParamChange('transactionVolumeFactor', value[0])}
          />
          <p className="text-sm text-muted-foreground">Impact of volume on price (0-1)</p>
        </div>
        <div className="space-y-2">
          <Label htmlFor="tokenVelocity">Token Velocity</Label>
          <Input 
            id="tokenVelocity" 
            type="number" 
            min={1}
            step={0.5}
            value={utilityTokenParams.tokenVelocity}
            onChange={(e) => handleUtilityParamChange('tokenVelocity', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">How often tokens change hands</p>
        </div>
      </div>
    </div>
  );

  const renderSecurityTokenForm = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="initialPriceSecurity">Initial Price (USD)</Label>
          <div className="flex items-center space-x-2">
            <span>$</span>
            <Input 
              id="initialPriceSecurity" 
              type="number" 
              min={0.001}
              step={0.1}
              value={securityTokenParams.initialPrice}
              onChange={(e) => handleSecurityParamChange('initialPrice', parseFloat(e.target.value))}
            />
          </div>
          <p className="text-sm text-muted-foreground">Starting price of token</p>
        </div>
        <div className="space-y-2">
          <Label htmlFor="initialSupplySecurity">Initial Supply</Label>
          <Input 
            id="initialSupplySecurity" 
            type="number" 
            min={1000}
            step={1000}
            value={securityTokenParams.initialSupply}
            onChange={(e) => handleSecurityParamChange('initialSupply', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">Total token supply</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="dividendYield">Dividend Yield (%)</Label>
            <span>{securityTokenParams.dividendYield}%</span>
          </div>
          <Slider
            id="dividendYield"
            min={0}
            max={20}
            step={0.1}
            value={[securityTokenParams.dividendYield]}
            onValueChange={(value) => handleSecurityParamChange('dividendYield', value[0])}
          />
          <p className="text-sm text-muted-foreground">Annual dividend percentage</p>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="marketGrowthRate">Market Growth Rate (%/year)</Label>
            <span>{securityTokenParams.marketGrowthRate}%</span>
          </div>
          <Slider
            id="marketGrowthRate"
            min={0}
            max={50}
            step={0.5}
            value={[securityTokenParams.marketGrowthRate]}
            onValueChange={(value) => handleSecurityParamChange('marketGrowthRate', value[0])}
          />
          <p className="text-sm text-muted-foreground">Annual market growth percentage</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="riskPremium">Risk Premium Rate (%)</Label>
            <span>{securityTokenParams.riskPremium}%</span>
          </div>
          <Slider
            id="riskPremium"
            min={0.1}
            max={20}
            step={0.1}
            value={[securityTokenParams.riskPremium]}
            onValueChange={(value) => handleSecurityParamChange('riskPremium', value[0])}
          />
          <p className="text-sm text-muted-foreground">Risk premium for discount rate</p>
        </div>
        <div className="space-y-2">
          <Label htmlFor="assetValue">Asset Value (USD)</Label>
          <div className="flex items-center space-x-2">
            <span>$</span>
            <Input 
              id="assetValue" 
              type="number" 
              min={100000}
              step={100000}
              value={securityTokenParams.assetValue}
              onChange={(e) => handleSecurityParamChange('assetValue', parseFloat(e.target.value))}
            />
          </div>
          <p className="text-sm text-muted-foreground">Value of underlying assets</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="equityMultiple">Equity Multiple</Label>
          <Input 
            id="equityMultiple" 
            type="number" 
            min={1}
            step={1}
            value={securityTokenParams.equityMultiple}
            onChange={(e) => handleSecurityParamChange('equityMultiple', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">Market cap to equity value ratio</p>
        </div>
      </div>
    </div>
  );

  const renderGovernanceTokenForm = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="initialPriceGovernance">Initial Price (USD)</Label>
          <div className="flex items-center space-x-2">
            <span>$</span>
            <Input 
              id="initialPriceGovernance" 
              type="number" 
              min={0.001}
              step={0.1}
              value={governanceTokenParams.initialPrice}
              onChange={(e) => handleGovernanceParamChange('initialPrice', parseFloat(e.target.value))}
            />
          </div>
          <p className="text-sm text-muted-foreground">Starting price of token</p>
        </div>
        <div className="space-y-2">
          <Label htmlFor="initialSupplyGovernance">Initial Supply</Label>
          <Input 
            id="initialSupplyGovernance" 
            type="number" 
            min={1000}
            step={1000}
            value={governanceTokenParams.initialSupply}
            onChange={(e) => handleGovernanceParamChange('initialSupply', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">Total token supply</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="initialStaking">Initial Staking Ratio (%)</Label>
            <span>{governanceTokenParams.initialStaking}%</span>
          </div>
          <Slider
            id="initialStaking"
            min={0}
            max={90}
            step={1}
            value={[governanceTokenParams.initialStaking]}
            onValueChange={(value) => handleGovernanceParamChange('initialStaking', value[0])}
          />
          <p className="text-sm text-muted-foreground">Percentage of tokens staked at launch</p>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="stakingReward">Staking Reward (%/year)</Label>
            <span>{governanceTokenParams.stakingReward}%</span>
          </div>
          <Slider
            id="stakingReward"
            min={0}
            max={30}
            step={0.5}
            value={[governanceTokenParams.stakingReward]}
            onValueChange={(value) => handleGovernanceParamChange('stakingReward', value[0])}
          />
          <p className="text-sm text-muted-foreground">Annual rewards for staking</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="votingRights">Voting Rights Multiplier</Label>
          <Input 
            id="votingRights" 
            type="number" 
            min={1}
            step={0.1}
            value={governanceTokenParams.votingRights}
            onChange={(e) => handleGovernanceParamChange('votingRights', parseFloat(e.target.value))}
          />
          <p className="text-sm text-muted-foreground">Voting power per token</p>
        </div>
        <div className="space-y-2">
          <Label htmlFor="networkValue">Initial Network Value (USD)</Label>
          <div className="flex items-center space-x-2">
            <span>$</span>
            <Input 
              id="networkValue" 
              type="number" 
              min={100000}
              step={100000}
              value={governanceTokenParams.networkValue}
              onChange={(e) => handleGovernanceParamChange('networkValue', parseFloat(e.target.value))}
            />
          </div>
          <p className="text-sm text-muted-foreground">Starting protocol/network value</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="governanceUtility">Governance Utility Factor</Label>
            <span>{governanceTokenParams.governanceUtility}</span>
          </div>
          <Slider
            id="governanceUtility"
            min={0}
            max={50}
            step={1}
            value={[governanceTokenParams.governanceUtility]}
            onValueChange={(value) => handleGovernanceParamChange('governanceUtility', value[0])}
          />
          <p className="text-sm text-muted-foreground">Value from governance rights</p>
        </div>
      </div>
    </div>
  );

  const renderSimulationControls = () => (
    <div className="space-y-4 py-4">
      <div className="space-y-2">
        <div className="flex justify-between">
          <Label htmlFor="simulationYears">Simulation Period (Years)</Label>
          <span>{simulationYears} years</span>
        </div>
        <Slider
          id="simulationYears"
          min={1}
          max={10}
          step={1}
          value={[simulationYears]}
          onValueChange={(value) => setSimulationYears(value[0])}
        />
      </div>
      
      <div className="flex space-x-2 justify-end">
        {showResults && (
          <Button variant="outline" onClick={resetSimulation}>
            Reset Simulation
          </Button>
        )}
        <Button onClick={runSimulation} className="bg-primary">
          Run Simulation
        </Button>
      </div>
    </div>
  );

  const renderUtilityTokenResults = () => (
    <div className="space-y-6">
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Price Evolution</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis yAxisId="left" label={{ value: 'Price ($)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value) => ['$' + value, 'Price']} />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} name="Token Price ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Market Cap & User Growth</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis 
                yAxisId="left" 
                label={{ value: 'Market Cap ($)', angle: -90, position: 'insideLeft' }} 
                tickFormatter={(value) => (value / 1000000).toFixed(0) + 'M'}
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                label={{ value: 'Users', angle: 90, position: 'insideRight' }} 
                tickFormatter={(value) => (value / 1000).toFixed(0) + 'K'}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'Market Cap ($)') {
                    return ['$' + (value / 1000000).toFixed(2) + 'M', name];
                  }
                  return [value.toLocaleString(), name];
                }} 
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="marketCap" stroke="#82ca9d" name="Market Cap ($)" />
              <Line yAxisId="right" type="monotone" dataKey="users" stroke="#ffc658" name="Users" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Transaction Volume & Circulation</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis 
                yAxisId="left" 
                label={{ value: 'Transaction Volume', angle: -90, position: 'insideLeft' }} 
                tickFormatter={(value) => (value / 1000).toFixed(0) + 'K'}
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                label={{ value: 'Circulating Supply', angle: 90, position: 'insideRight' }} 
                tickFormatter={(value) => (value / 1000000).toFixed(0) + 'M'}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'Transaction Volume') {
                    return [value.toLocaleString(), name];
                  } else if (name === 'Circulating Supply') {
                    return [(value / 1000000).toFixed(2) + 'M', name];
                  }
                  return [value, name];
                }} 
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="transactionVolume" stroke="#ff7300" name="Transaction Volume" />
              <Line yAxisId="right" type="monotone" dataKey="circulatingSupply" stroke="#0088aa" name="Circulating Supply" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Data Table</h3>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Year</TableHead>
                <TableHead>Users</TableHead>
                <TableHead>Price ($)</TableHead>
                <TableHead>Market Cap ($)</TableHead>
                <TableHead>Circulating Supply</TableHead>
                <TableHead>Transaction Volume</TableHead>
                <TableHead>Token Velocity</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {simulationData.map((row, i) => (
                <TableRow key={i}>
                  <TableCell>{row.year}</TableCell>
                  <TableCell>{row.users.toLocaleString()}</TableCell>
                  <TableCell>${row.price.toFixed(3)}</TableCell>
                  <TableCell>${(row.marketCap / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>{(row.circulatingSupply / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>{(row.transactionVolume / 1000).toFixed(1)}K</TableCell>
                  <TableCell>{row.tokenVelocity}x</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );

  const renderSecurityTokenResults = () => (
    <div className="space-y-6">
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Price Evolution</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis yAxisId="left" label={{ value: 'Price ($)', angle: -90, position: 'insideLeft' }} />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                label={{ value: 'Dividend/Token ($)', angle: 90, position: 'insideRight' }} 
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'Token Price ($)' || name === 'Dividend per Token ($)') {
                    return ['$' + value, name];
                  }
                  return [value, name];
                }}
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} name="Token Price ($)" />
              <Line yAxisId="right" type="monotone" dataKey="dividendPerToken" stroke="#82ca9d" name="Dividend per Token ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Asset Value & Market Cap</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis 
                yAxisId="left" 
                label={{ value: 'Value ($)', angle: -90, position: 'insideLeft' }} 
                tickFormatter={(value) => (value / 1000000).toFixed(0) + 'M'}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'Asset Value ($)' || name === 'Market Cap ($)' || name === 'Equity Value ($)') {
                    return ['$' + (value / 1000000).toFixed(2) + 'M', name];
                  }
                  return [value, name];
                }} 
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="assetValue" stroke="#8884d8" name="Asset Value ($)" />
              <Line yAxisId="left" type="monotone" dataKey="marketCap" stroke="#82ca9d" name="Market Cap ($)" />
              <Line yAxisId="left" type="monotone" dataKey="equityValue" stroke="#ffc658" name="Equity Value ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Data Table</h3>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Year</TableHead>
                <TableHead>Price ($)</TableHead>
                <TableHead>Market Cap ($)</TableHead>
                <TableHead>Circulating Supply</TableHead>
                <TableHead>Asset Value ($)</TableHead>
                <TableHead>Dividend/Token ($)</TableHead>
                <TableHead>Equity Value ($)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {simulationData.map((row, i) => (
                <TableRow key={i}>
                  <TableCell>{row.year}</TableCell>
                  <TableCell>${row.price.toFixed(3)}</TableCell>
                  <TableCell>${(row.marketCap / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>{(row.circulatingSupply / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>${(row.assetValue / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>${row.dividendPerToken.toFixed(4)}</TableCell>
                  <TableCell>${(row.equityValue / 1000000).toFixed(2)}M</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );

  const renderGovernanceTokenResults = () => (
    <div className="space-y-6">
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Price Evolution</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis yAxisId="left" label={{ value: 'Price ($)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value) => ['$' + value, 'Price']} />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} name="Token Price ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Staking & Voting Power</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis 
                yAxisId="left" 
                label={{ value: 'Staking Ratio (%)', angle: -90, position: 'insideLeft' }} 
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                label={{ value: 'Voting Power', angle: 90, position: 'insideRight' }} 
                tickFormatter={(value) => (value / 1000000).toFixed(1) + 'M'}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'Staking Ratio (%)') {
                    return [value + '%', name];
                  } else if (name === 'Voting Power') {
                    return [(value / 1000000).toFixed(2) + 'M', name];
                  }
                  return [value, name];
                }} 
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="stakingRatio" stroke="#82ca9d" name="Staking Ratio (%)" />
              <Line yAxisId="right" type="monotone" dataKey="votingPower" stroke="#8884d8" name="Voting Power" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Network Value & Market Cap</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
              <YAxis 
                yAxisId="left" 
                label={{ value: 'Value ($)', angle: -90, position: 'insideLeft' }} 
                tickFormatter={(value) => (value / 1000000).toFixed(0) + 'M'}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'Network Value ($)' || name === 'Market Cap ($)') {
                    return ['$' + (value / 1000000).toFixed(2) + 'M', name];
                  }
                  return [value, name];
                }} 
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="networkValue" stroke="#8884d8" name="Network Value ($)" />
              <Line yAxisId="left" type="monotone" dataKey="marketCap" stroke="#82ca9d" name="Market Cap ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Data Table</h3>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Year</TableHead>
                <TableHead>Price ($)</TableHead>
                <TableHead>Market Cap ($)</TableHead>
                <TableHead>Circulating Supply</TableHead>
                <TableHead>Staked Tokens</TableHead>
                <TableHead>Staking Ratio (%)</TableHead>
                <TableHead>Network Value ($)</TableHead>
                <TableHead>Voting Power</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {simulationData.map((row, i) => (
                <TableRow key={i}>
                  <TableCell>{row.year}</TableCell>
                  <TableCell>${row.price.toFixed(3)}</TableCell>
                  <TableCell>${(row.marketCap / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>{(row.circulatingSupply / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>{(row.stakedTokens / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>{row.stakingRatio}%</TableCell>
                  <TableCell>${(row.networkValue / 1000000).toFixed(2)}M</TableCell>
                  <TableCell>{(row.votingPower / 1000000).toFixed(2)}M</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );

  const renderModelDescription = () => {
    switch (activeTab) {
      case "utility-token":
        return (
          <div className="rounded-lg border p-4 bg-muted/50 mb-4">
            <div className="flex items-start space-x-2">
              <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
              <div>
                <h3 className="font-medium">Utility Token Model</h3>
                <p className="text-sm text-muted-foreground">
                  This model simulates a utility token where value is derived from the token's use within an ecosystem. 
                  The price is influenced by user growth, network effects, and transaction volume. The model accounts 
                  for factors like token velocity and utility value per user.
                </p>
              </div>
            </div>
          </div>
        );
      case "security-token":
        return (
          <div className="rounded-lg border p-4 bg-muted/50 mb-4">
            <div className="flex items-start space-x-2">
              <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
              <div>
                <h3 className="font-medium">Security Token Model</h3>
                <p className="text-sm text-muted-foreground">
                  This model simulates a security token representing ownership of an underlying asset. 
                  The price is influenced by dividend yield, market growth rate, and risk premium. 
                  The model applies discounted cash flow and equity valuation principles.
                </p>
              </div>
            </div>
          </div>
        );
      case "governance-token":
        return (
          <div className="rounded-lg border p-4 bg-muted/50 mb-4">
            <div className="flex items-start space-x-2">
              <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
              <div>
                <h3 className="font-medium">Governance Token Model</h3>
                <p className="text-sm text-muted-foreground">
                  This model simulates a governance token used for voting and protocol governance. 
                  The price is influenced by staking incentives, voting power, and network value growth. 
                  The model accounts for governance utility and staking dynamics.
                </p>
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  const renderResultsForModel = () => {
    switch (activeTab) {
      case "utility-token":
        return renderUtilityTokenResults();
      case "security-token":
        return renderSecurityTokenResults();
      case "governance-token":
        return renderGovernanceTokenResults();
      default:
        return null;
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Economic Models</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Tokenomics Economic Models</CardTitle>
          <CardDescription>Simulate and analyze different token economic models</CardDescription>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid grid-cols-3 w-full">
              <TabsTrigger value="utility-token" className="flex items-center gap-1">
                <Coins className="h-4 w-4" />
                <span>Utility Token</span>
              </TabsTrigger>
              <TabsTrigger value="security-token" className="flex items-center gap-1">
                <DollarSign className="h-4 w-4" />
                <span>Security Token</span>
              </TabsTrigger>
              <TabsTrigger value="governance-token" className="flex items-center gap-1">
                <PieChart className="h-4 w-4" />
                <span>Governance Token</span>
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </CardHeader>
        <CardContent>
          {renderModelDescription()}
          <TabsContent value="utility-token">
            {renderUtilityTokenForm()}
          </TabsContent>
          <TabsContent value="security-token">
            {renderSecurityTokenForm()}
          </TabsContent>
          <TabsContent value="governance-token">
            {renderGovernanceTokenForm()}
          </TabsContent>
          
          {renderSimulationControls()}
          
          {showResults && (
            <div className="mt-6 pt-6 border-t">
              <h2 className="text-2xl font-bold mb-4">Simulation Results</h2>
              {renderResultsForModel()}
              <div className="flex space-x-2 justify-end mt-6">
                <Button variant="outline" className="flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  <span>Export Report</span>
                </Button>
                <Button variant="outline" className="flex items-center gap-2">
                  <FileDown className="h-4 w-4" />
                  <span>Download CSV</span>
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}