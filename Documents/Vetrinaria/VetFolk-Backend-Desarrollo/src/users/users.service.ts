import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { User } from './user.entity';
import { Repository } from 'typeorm';
import { createUserDto } from './dto/createUser.dto';
import { LoginDto } from './dto/login.dto';
@Injectable()
export class UsersService {
    constructor(@InjectRepository(User)private userRepository: Repository<User>){}

    createUser(user:createUserDto){
        const newUser = this.userRepository.create(user)
        return this.userRepository.save(newUser)
    }

    findByEmail(correo:string){
        return this.userRepository.findOneBy({correo})
    }

   async validar(LoginDto:LoginDto): Promise<boolean>{
        const { correo, password } = LoginDto;
    const user = await this.findByEmail(correo);
    if (user && user.password === password) {
      return true; // La contraseña coincide
    }
    return false; // La contraseña no coincide
  
    }
}
