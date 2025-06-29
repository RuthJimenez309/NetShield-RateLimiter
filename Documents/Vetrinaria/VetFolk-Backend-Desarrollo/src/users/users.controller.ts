import { Body, Controller, Post, HttpStatus, Res } from '@nestjs/common';
import { Response } from 'express';
import { createUserDto } from './dto/createUser.dto';
import { UsersService } from './users.service';
import { LoginDto } from './dto/login.dto';

@Controller('users')
export class UsersController {
  constructor(private userService: UsersService) {}

  @Post('create')
  createUser(@Body() newUser: createUserDto) {
    return this.userService.createUser(newUser);
  }

  @Post('login')
  async login(@Body() loginDto: LoginDto, @Res() res: Response) {
    const isValid = await this.userService.validar(loginDto);

    if (isValid) {
      return res.status(HttpStatus.OK).json({
        success: true,
        message: 'Login successful',
        // Aquí puedes agregar más información como un token JWT si es necesario
      });
    } else {
      return res.status(HttpStatus.UNAUTHORIZED).json({
        success: false,
        message: 'Invalid email or password',
      });
    }
  }
}
