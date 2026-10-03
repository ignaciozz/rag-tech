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
