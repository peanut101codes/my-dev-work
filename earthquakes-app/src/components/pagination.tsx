import Pagination from '@mui/material/Pagination';

type BasicPaginationProps = {
  cardsPerPage: number;
  totalCards: number;
  page: number;
  setPage: (page: number) => void;
};

export default function BasicPagination({ cardsPerPage, totalCards, page, setPage }: BasicPaginationProps) {
  const totalPages = Math.ceil(totalCards / cardsPerPage);
  const handleChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  return (
    <>
      {totalPages > 1 && (
          <Pagination count={totalPages} color="primary" page={page} onChange={handleChange} />
      )}
    </>
  );
}
