export type Source = {
  n: number;
  doc: string;
  page: number;
};

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export type DocumentInfo = {
  id: string;
  title: string;
  technology: string;
  version: string | null;
  fileType: string;
  chunksCount: number;
};
