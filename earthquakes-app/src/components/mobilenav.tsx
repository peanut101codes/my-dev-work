'use client'
import * as React from 'react';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import MenuItem from '@mui/material/MenuItem';
import AdbIcon from '@mui/icons-material/Public';
import HomeIcon from '@mui/icons-material/HomeOutlined';
import AboutIcon from '@mui/icons-material/InfoOutlined';
import PageIcon from '@mui/icons-material/ArticleOutlined';
import Link from 'next/link';

interface MobileNavProps {
  pages: string[];
}

function MobileNav({ pages }: MobileNavProps) {
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  return (
    <>
      <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
        <IconButton
          size="large"
          aria-label="account of current user"
          aria-controls="menu-appbar"
          aria-haspopup="true"
          onClick={handleOpenNavMenu}
          color="inherit"
        >
          <MenuIcon />
        </IconButton>
        <Menu
          id="menu-appbar"
          anchorEl={anchorElNav}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
          keepMounted
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          open={Boolean(anchorElNav)}
          onClose={handleCloseNavMenu}
          sx={{ display: { xs: 'block', md: 'none' } }}
        >
          <MenuItem onClick={handleCloseNavMenu}>
                <Link
                  href="/"
                  className="text-black hover:underline inline-flex items-center"
                  style={{ display: 'flex', alignItems: 'center' }}
                >
                  <HomeIcon sx={{ mr: 1 }} />
                  <Typography sx={{ textAlign: 'center' }}>Home</Typography>
                </Link>
            </MenuItem>
          {pages.map((page) => (
            <MenuItem key={page} onClick={handleCloseNavMenu}>
                <Link
                    href={`/${page.toLowerCase()}`}
                    className="text-black hover:underline inline-block"
                    style={{ display: 'flex', alignItems: 'center' }}
                >
                    {page.toLowerCase() === 'about' ? (
                      <AboutIcon sx={{ mr: 1 }} />
                    ) : (
                      <PageIcon sx={{ mr: 1 }} />
                    )}
                    <Typography sx={{ textAlign: 'center' }}>{page}</Typography>
                </Link>
            </MenuItem>
          ))}
        </Menu>
      </Box>
      <AdbIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
        <Typography
            variant="h5"
            noWrap
            component="a"
            href="/"
            sx={{
            mr: 2,
            display: { xs: 'flex', md: 'none' },
            flexGrow: 1,
            fontFamily: 'monospace',
            fontWeight: 700,
            letterSpacing: '.3rem',
            color: 'inherit',
            textDecoration: 'none',
            }}
        >
            Earthquakes
        </Typography>
    </>
   
  );
}
export default MobileNav;
