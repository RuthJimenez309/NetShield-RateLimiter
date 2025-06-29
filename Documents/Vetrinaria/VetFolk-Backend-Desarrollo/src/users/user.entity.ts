import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

@Entity()
export class User{
    @PrimaryGeneratedColumn()
    id: number

    @Column()
    primerNombre: string

    @Column({nullable: true})
    segundoNombre: string

    @Column()
    primerApellido: string

    @Column({nullable: true})
    segundoApellido: string

    @Column()
    telefono: string

    @Column()
    correo: string

    @Column()
    password: string

}