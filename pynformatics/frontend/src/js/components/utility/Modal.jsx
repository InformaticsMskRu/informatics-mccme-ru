import { Modal as AntdModal } from 'antd';

import ModalStyle, { ModalContent } from '../../isomorphic/containers/Feedback/Modal/modal.style';


const Modal = ModalStyle(AntdModal);

export default Modal;
export {
  ModalStyle,
  ModalContent,
};
