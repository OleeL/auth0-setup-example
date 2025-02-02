const testConfig = {
  apiUri: "http://localhost:5999",
} as const;

const productionConfig = {
  apiUri: "https://<hostname>",
} as const;

const config = {
  ...(import.meta.env.PROD ? productionConfig : testConfig),
};

export default config;
