
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'app.lovable.bed97fd033e44f1693b0ed6a6a22afbe',
  appName: 'tokenomics-lab-innovation',
  webDir: 'dist',
  server: {
    url: 'https://bed97fd0-33e4-4f16-93b0-ed6a6a22afbe.lovableproject.com?forceHideBadge=true',
    cleartext: true
  },
  android: {
    buildOptions: {
      keystorePath: undefined,
      keystoreAlias: undefined,
      keystorePassword: undefined,
      keystoreAliasPassword: undefined,
      releaseType: undefined,
    }
  }
};

export default config;
